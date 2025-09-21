"""
Inventory management endpoints for CRUD operations on inventory items.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_user, require_manager
from app.models.inventory import InventoryItem, InventoryUpdate
from app.models.supplier import Supplier
from app.schemas.inventory import (
    InventoryItem as InventoryItemSchema,
    InventoryItemCreate,
    InventoryItemUpdate,
    InventoryItemList,
    StockAdjustment,
    InventoryUpdate as InventoryUpdateSchema,
    LowStockAlert
)
from app.core.exceptions import ItemNotFoundException, InsufficientStockException

router = APIRouter()


@router.get("/items", response_model=InventoryItemList)
async def get_inventory_items(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    low_stock_only: bool = Query(False),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get paginated list of inventory items with optional filtering."""
    offset = (page - 1) * size
    
    # Build query
    query = select(InventoryItem).options(selectinload(InventoryItem.supplier))
    
    # Apply filters
    filters = []
    if search:
        search_filter = or_(
            InventoryItem.name.ilike(f"%{search}%"),
            InventoryItem.sku.ilike(f"%{search}%"),
            InventoryItem.barcode.ilike(f"%{search}%")
        )
        filters.append(search_filter)
    
    if category:
        filters.append(InventoryItem.category == category)
    
    if low_stock_only:
        filters.append(InventoryItem.quantity_in_stock <= InventoryItem.reorder_point)
    
    if filters:
        query = query.where(and_(*filters))
    
    # Get total count
    count_query = select(func.count(InventoryItem.id))
    if filters:
        count_query = count_query.where(and_(*filters))
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Get paginated results
    query = query.offset(offset).limit(size).order_by(InventoryItem.name)
    result = await db.execute(query)
    items = result.scalars().all()
    
    return InventoryItemList(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/items/{item_id}", response_model=InventoryItemSchema)
async def get_inventory_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific inventory item by ID."""
    stmt = select(InventoryItem).options(selectinload(InventoryItem.supplier)).where(InventoryItem.id == item_id)
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    
    if not item:
        raise ItemNotFoundException(f"Inventory item with ID {item_id} not found")
    
    return item


@router.post("/items", response_model=InventoryItemSchema)
async def create_inventory_item(
    item_data: InventoryItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_manager)
):
    """Create a new inventory item."""
    # Check if SKU already exists
    stmt = select(InventoryItem).where(InventoryItem.sku == item_data.sku)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item with this SKU already exists"
        )
    
    # Check if barcode already exists (if provided)
    if item_data.barcode:
        stmt = select(InventoryItem).where(InventoryItem.barcode == item_data.barcode)
        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item with this barcode already exists"
            )
    
    # Create new item
    item = InventoryItem(**item_data.dict())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    
    return item


@router.put("/items/{item_id}", response_model=InventoryItemSchema)
async def update_inventory_item(
    item_id: int,
    item_data: InventoryItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_manager)
):
    """Update an existing inventory item."""
    stmt = select(InventoryItem).where(InventoryItem.id == item_id)
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    
    if not item:
        raise ItemNotFoundException(f"Inventory item with ID {item_id} not found")
    
    # Check SKU uniqueness if being updated
    if item_data.sku and item_data.sku != item.sku:
        stmt = select(InventoryItem).where(InventoryItem.sku == item_data.sku)
        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item with this SKU already exists"
            )
    
    # Check barcode uniqueness if being updated
    if item_data.barcode and item_data.barcode != item.barcode:
        stmt = select(InventoryItem).where(InventoryItem.barcode == item_data.barcode)
        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item with this barcode already exists"
            )
    
    # Update item
    update_data = item_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    await db.commit()
    await db.refresh(item)
    
    return item


@router.delete("/items/{item_id}")
async def delete_inventory_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_manager)
):
    """Delete an inventory item."""
    stmt = select(InventoryItem).where(InventoryItem.id == item_id)
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    
    if not item:
        raise ItemNotFoundException(f"Inventory item with ID {item_id} not found")
    
    await db.delete(item)
    await db.commit()
    
    return {"message": "Inventory item deleted successfully"}


@router.post("/items/{item_id}/adjust-stock")
async def adjust_stock(
    item_id: int,
    adjustment: StockAdjustment,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Adjust stock quantity for an inventory item."""
    stmt = select(InventoryItem).where(InventoryItem.id == item_id)
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    
    if not item:
        raise ItemNotFoundException(f"Inventory item with ID {item_id} not found")
    
    if not item.is_tracked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This item is not tracked for stock levels"
        )
    
    new_quantity = item.quantity_in_stock + adjustment.quantity_change
    
    if new_quantity < 0:
        raise InsufficientStockException(
            f"Insufficient stock. Current: {item.quantity_in_stock}, "
            f"Requested reduction: {abs(adjustment.quantity_change)}"
        )
    
    # Record the change
    inventory_update = InventoryUpdate(
        item_id=item_id,
        user_id=current_user["user_id"],
        change_type=adjustment.reason,
        quantity_change=adjustment.quantity_change,
        previous_quantity=item.quantity_in_stock,
        new_quantity=new_quantity,
        reason=adjustment.reason,
        reference_number=adjustment.reference_number,
        notes=adjustment.notes
    )
    
    # Update stock
    item.quantity_in_stock = new_quantity
    
    db.add(inventory_update)
    await db.commit()
    
    return {"message": "Stock adjusted successfully", "new_quantity": new_quantity}


@router.get("/items/low-stock", response_model=List[LowStockAlert])
async def get_low_stock_items(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all items that are below their reorder point."""
    stmt = select(InventoryItem).options(selectinload(InventoryItem.supplier)).where(
        InventoryItem.quantity_in_stock <= InventoryItem.reorder_point
    )
    result = await db.execute(stmt)
    items = result.scalars().all()
    
    alerts = []
    for item in items:
        alerts.append(LowStockAlert(
            item_id=item.id,
            sku=item.sku,
            name=item.name,
            current_stock=item.quantity_in_stock,
            reorder_point=item.reorder_point,
            minimum_stock_level=item.minimum_stock_level,
            supplier_name=item.supplier.name if item.supplier else None
        ))
    
    return alerts


@router.get("/items/{item_id}/history", response_model=List[InventoryUpdateSchema])
async def get_item_history(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get stock movement history for an inventory item."""
    stmt = select(InventoryUpdate).where(InventoryUpdate.item_id == item_id).order_by(InventoryUpdate.created_at.desc())
    result = await db.execute(stmt)
    updates = result.scalars().all()
    
    return updates
