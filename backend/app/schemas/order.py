"""
Pydantic schemas for order-related API endpoints.
"""

from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from app.models.order import OrderType, OrderStatus


class OrderItemBase(BaseModel):
    """Base order item schema."""
    item_id: int
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., gt=0)
    notes: Optional[str] = None


class OrderItemCreate(OrderItemBase):
    """Schema for creating order items."""
    pass


class OrderItemUpdate(BaseModel):
    """Schema for updating order items."""
    quantity: Optional[int] = Field(None, gt=0)
    unit_price: Optional[Decimal] = Field(None, gt=0)
    notes: Optional[str] = None


class OrderItem(OrderItemBase):
    """Schema for order item response."""
    id: int
    total_price: Decimal
    
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    """Base order schema with common fields."""
    order_type: OrderType
    status: OrderStatus = OrderStatus.PENDING
    expected_delivery_date: Optional[datetime] = None
    shipping_address: Optional[str] = None
    shipping_city: Optional[str] = Field(None, max_length=100)
    shipping_state: Optional[str] = Field(None, max_length=100)
    shipping_country: Optional[str] = Field(None, max_length=100)
    shipping_postal_code: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = None
    internal_notes: Optional[str] = None
    tracking_number: Optional[str] = Field(None, max_length=100)
    supplier_id: Optional[int] = None


class OrderCreate(OrderBase):
    """Schema for creating a new order."""
    order_items: List[OrderItemCreate] = Field(..., min_items=1)


class OrderUpdate(BaseModel):
    """Schema for updating order information."""
    status: Optional[OrderStatus] = None
    expected_delivery_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None
    shipping_address: Optional[str] = None
    shipping_city: Optional[str] = Field(None, max_length=100)
    shipping_state: Optional[str] = Field(None, max_length=100)
    shipping_country: Optional[str] = Field(None, max_length=100)
    shipping_postal_code: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = None
    internal_notes: Optional[str] = None
    tracking_number: Optional[str] = Field(None, max_length=100)
    supplier_id: Optional[int] = None


class Order(OrderBase):
    """Schema for order response."""
    id: int
    order_number: str
    total_amount: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal
    order_date: datetime
    actual_delivery_date: Optional[datetime] = None
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    order_items: List[OrderItem] = []
    
    class Config:
        from_attributes = True


class OrderList(BaseModel):
    """Schema for paginated order list response."""
    orders: List[Order]
    total: int
    page: int
    size: int
    pages: int


class OrderSummary(BaseModel):
    """Schema for order summary statistics."""
    total_orders: int
    pending_orders: int
    completed_orders: int
    cancelled_orders: int
    total_value: Decimal
    average_order_value: Decimal
