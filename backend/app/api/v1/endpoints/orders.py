"""
Order management endpoints for CRUD operations on orders.
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from decimal import Decimal

from app.core.database import get_db
from app.core.security import get_current_user, require_manager
from app.models.order import Order, OrderItem, OrderType, OrderStatus
from app.models.inventory import InventoryItem
from app.models.supplier import Supplier
from app.schemas.order import (
    Order as OrderSchema,
    OrderCreate,
    OrderUpdate,
    OrderList,
    OrderSummary
)
from app.core.exceptions import OrderNotFoundException, ItemNotFoundException

router = APIRouter()


@router.get("/", response_model=OrderList)
async def get_orders(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    order_type: Optional[OrderType] = Query(None),
    status: Optional[OrderStatus] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get paginated list of orders with optional filtering."""
    offset = (page - 1) * size
    
    # Build query
    query = select(Order).options(
        selectinload(Order.order_items).selectinload(OrderItem.item),
        selectinload(Order.supplier),
        selectinload(Order.user)
    )
    
    # Apply filters
    filters = []
    if order_type:
        filters.append(Order.order_type == order_type)
    
    if status:
        filters.append(Order.status == status)
    
    if search:
        search_filter = or_(
            Order.order_number.ilike(f"%{search}%"),
            Order.tracking_number.ilike(f"%{search}%")
        )
        filters.append(search_filter)
    
    if filters:
        query = query.where(and_(*filters))
    
    # Get total count
    count_query = select(func.count(Order.id))
    if filters:
        count_query = count_query.where(and_(*filters))
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Get paginated results
    query = query.offset(offset).limit(size).order_by(Order.order_date.desc())
    result = await db.execute(query)
    orders = result.scalars().all()
    
    return OrderList(
        orders=orders,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/{order_id}", response_model=OrderSchema)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific order by ID."""
    stmt = select(Order).options(
        selectinload(Order.order_items).selectinload(OrderItem.item),
        selectinload(Order.supplier),
        selectinload(Order.user)
    ).where(Order.id == order_id)
    
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    
    if not order:
        raise OrderNotFoundException(f"Order with ID {order_id} not found")
    
    return order


@router.post("/", response_model=OrderSchema)
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new order."""
    # Generate order number
    order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{current_user['user_id']:04d}"
    
    # Calculate totals
    total_amount = Decimal('0')
    for item in order_data.order_items:
        item_total = item.quantity * item.unit_price
        total_amount += item_total
    
    # Create order
    order = Order(
        order_number=order_number,
        order_type=order_data.order_type,
        status=order_data.status,
        total_amount=total_amount,
        expected_delivery_date=order_data.expected_delivery_date,
        shipping_address=order_data.shipping_address,
        shipping_city=order_data.shipping_city,
        shipping_state=order_data.shipping_state,
        shipping_country=order_data.shipping_country,
        shipping_postal_code=order_data.shipping_postal_code,
        notes=order_data.notes,
        internal_notes=order_data.internal_notes,
        tracking_number=order_data.tracking_number,
        supplier_id=order_data.supplier_id,
        user_id=current_user['user_id']
    )
    
    db.add(order)
    await db.flush()  # Get the order ID
    
    # Create order items
    for item_data in order_data.order_items:
        # Verify item exists
        stmt = select(InventoryItem).where(InventoryItem.id == item_data.item_id)
        result = await db.execute(stmt)
        item = result.scalar_one_or_none()
        
        if not item:
            raise ItemNotFoundException(f"Inventory item with ID {item_data.item_id} not found")
        
        order_item = OrderItem(
            order_id=order.id,
            item_id=item_data.item_id,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            total_price=item_data.quantity * item_data.unit_price,
            notes=item_data.notes
        )
        db.add(order_item)
    
    await db.commit()
    await db.refresh(order)
    
    return order


@router.put("/{order_id}", response_model=OrderSchema)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_manager)
):
    """Update an existing order."""
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    
    if not order:
        raise OrderNotFoundException(f"Order with ID {order_id} not found")
    
    # Update order
    update_data = order_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    
    await db.commit()
    await db.refresh(order)
    
    return order


@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_manager)
):
    """Delete an order."""
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    
    if not order:
        raise OrderNotFoundException(f"Order with ID {order_id} not found")
    
    # Only allow deletion of pending orders
    if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending orders can be deleted"
        )
    
    await db.delete(order)
    await db.commit()
    
    return {"message": "Order deleted successfully"}


@router.patch("/{order_id}/status")
async def update_order_status(
    order_id: int,
    new_status: OrderStatus,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_manager)
):
    """Update order status."""
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    
    if not order:
        raise OrderNotFoundException(f"Order with ID {order_id} not found")
    
    # Update stock levels when order is delivered
    if new_status == OrderStatus.DELIVERED and order.status != OrderStatus.DELIVERED:
        await _update_stock_for_delivered_order(order, db, current_user)
    
    order.status = new_status
    if new_status == OrderStatus.DELIVERED:
        order.actual_delivery_date = datetime.utcnow()
    
    await db.commit()
    
    return {"message": f"Order status updated to {new_status.value}"}


@router.get("/summary/stats", response_model=OrderSummary)
async def get_order_summary(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get order summary statistics."""
    # Total orders
    total_orders_stmt = select(func.count(Order.id))
    total_orders_result = await db.execute(total_orders_stmt)
    total_orders = total_orders_result.scalar()
    
    # Orders by status
    pending_stmt = select(func.count(Order.id)).where(Order.status == OrderStatus.PENDING)
    pending_result = await db.execute(pending_stmt)
    pending_orders = pending_result.scalar()
    
    completed_stmt = select(func.count(Order.id)).where(Order.status == OrderStatus.DELIVERED)
    completed_result = await db.execute(completed_stmt)
    completed_orders = completed_result.scalar()
    
    cancelled_stmt = select(func.count(Order.id)).where(Order.status == OrderStatus.CANCELLED)
    cancelled_result = await db.execute(cancelled_stmt)
    cancelled_orders = cancelled_result.scalar()
    
    # Total value
    total_value_stmt = select(func.sum(Order.total_amount))
    total_value_result = await db.execute(total_value_stmt)
    total_value = total_value_result.scalar() or Decimal('0')
    
    # Average order value
    avg_value = total_value / total_orders if total_orders > 0 else Decimal('0')
    
    return OrderSummary(
        total_orders=total_orders,
        pending_orders=pending_orders,
        completed_orders=completed_orders,
        cancelled_orders=cancelled_orders,
        total_value=total_value,
        average_order_value=avg_value
    )


async def _update_stock_for_delivered_order(order: Order, db: AsyncSession, current_user: dict):
    """Update stock levels when an order is delivered."""
    from app.models.inventory import InventoryUpdate
    
    for order_item in order.order_items:
        item = order_item.item
        
        if not item.is_tracked:
            continue
        
        # For purchase orders, increase stock
        if order.order_type == OrderType.PURCHASE:
            quantity_change = order_item.quantity
            change_type = "purchase"
        # For sales orders, decrease stock
        elif order.order_type == OrderType.SALE:
            quantity_change = -order_item.quantity
            change_type = "sale"
        else:
            continue
        
        new_quantity = item.quantity_in_stock + quantity_change
        
        # Record the change
        inventory_update = InventoryUpdate(
            item_id=item.id,
            user_id=current_user['user_id'],
            change_type=change_type,
            quantity_change=quantity_change,
            previous_quantity=item.quantity_in_stock,
            new_quantity=new_quantity,
            reason=f"Order {order.order_number} delivered",
            reference_number=order.order_number
        )
        
        # Update stock
        item.quantity_in_stock = new_quantity
        
        db.add(inventory_update)
