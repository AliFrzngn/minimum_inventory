"""
Supplier management endpoints for CRUD operations on suppliers.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_

from app.core.database import get_db
from app.core.security import get_current_user, require_manager
from app.models.supplier import Supplier
from app.schemas.supplier import (
    Supplier as SupplierSchema,
    SupplierCreate,
    SupplierUpdate,
    SupplierList
)
from app.core.exceptions import SupplierNotFoundException

router = APIRouter()


@router.get("/", response_model=SupplierList)
async def get_suppliers(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    active_only: bool = Query(True),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get paginated list of suppliers with optional filtering."""
    offset = (page - 1) * size
    
    # Build query
    query = select(Supplier)
    
    # Apply filters
    filters = []
    if search:
        search_filter = or_(
            Supplier.name.ilike(f"%{search}%"),
            Supplier.contact_person.ilike(f"%{search}%"),
            Supplier.email.ilike(f"%{search}%")
        )
        filters.append(search_filter)
    
    if active_only:
        filters.append(Supplier.is_active == True)
    
    if filters:
        query = query.where(and_(*filters))
    
    # Get total count
    count_query = select(func.count(Supplier.id))
    if filters:
        count_query = count_query.where(and_(*filters))
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Get paginated results
    query = query.offset(offset).limit(size).order_by(Supplier.name)
    result = await db.execute(query)
    suppliers = result.scalars().all()
    
    return SupplierList(
        suppliers=suppliers,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/{supplier_id}", response_model=SupplierSchema)
async def get_supplier(
    supplier_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific supplier by ID."""
    stmt = select(Supplier).where(Supplier.id == supplier_id)
    result = await db.execute(stmt)
    supplier = result.scalar_one_or_none()
    
    if not supplier:
        raise SupplierNotFoundException(f"Supplier with ID {supplier_id} not found")
    
    return supplier


@router.post("/", response_model=SupplierSchema)
async def create_supplier(
    supplier_data: SupplierCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_manager)
):
    """Create a new supplier."""
    # Check if supplier with same name already exists
    stmt = select(Supplier).where(Supplier.name == supplier_data.name)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supplier with this name already exists"
        )
    
    # Create new supplier
    supplier = Supplier(**supplier_data.dict())
    db.add(supplier)
    await db.commit()
    await db.refresh(supplier)
    
    return supplier


@router.put("/{supplier_id}", response_model=SupplierSchema)
async def update_supplier(
    supplier_id: int,
    supplier_data: SupplierUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_manager)
):
    """Update an existing supplier."""
    stmt = select(Supplier).where(Supplier.id == supplier_id)
    result = await db.execute(stmt)
    supplier = result.scalar_one_or_none()
    
    if not supplier:
        raise SupplierNotFoundException(f"Supplier with ID {supplier_id} not found")
    
    # Check name uniqueness if being updated
    if supplier_data.name and supplier_data.name != supplier.name:
        stmt = select(Supplier).where(Supplier.name == supplier_data.name)
        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Supplier with this name already exists"
            )
    
    # Update supplier
    update_data = supplier_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(supplier, field, value)
    
    await db.commit()
    await db.refresh(supplier)
    
    return supplier


@router.delete("/{supplier_id}")
async def delete_supplier(
    supplier_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_manager)
):
    """Delete a supplier."""
    stmt = select(Supplier).where(Supplier.id == supplier_id)
    result = await db.execute(stmt)
    supplier = result.scalar_one_or_none()
    
    if not supplier:
        raise SupplierNotFoundException(f"Supplier with ID {supplier_id} not found")
    
    # Check if supplier has associated items
    from app.models.inventory import InventoryItem
    stmt = select(func.count(InventoryItem.id)).where(InventoryItem.supplier_id == supplier_id)
    result = await db.execute(stmt)
    item_count = result.scalar()
    
    if item_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete supplier. {item_count} inventory items are associated with this supplier."
        )
    
    await db.delete(supplier)
    await db.commit()
    
    return {"message": "Supplier deleted successfully"}


@router.patch("/{supplier_id}/toggle-status")
async def toggle_supplier_status(
    supplier_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_manager)
):
    """Toggle supplier active status."""
    stmt = select(Supplier).where(Supplier.id == supplier_id)
    result = await db.execute(stmt)
    supplier = result.scalar_one_or_none()
    
    if not supplier:
        raise SupplierNotFoundException(f"Supplier with ID {supplier_id} not found")
    
    supplier.is_active = not supplier.is_active
    await db.commit()
    
    return {
        "message": f"Supplier {'activated' if supplier.is_active else 'deactivated'} successfully",
        "is_active": supplier.is_active
    }
