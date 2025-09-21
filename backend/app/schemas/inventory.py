"""
Pydantic schemas for inventory-related API endpoints.
"""

from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from app.models.inventory import ItemCategory, ItemStatus


class InventoryItemBase(BaseModel):
    """Base inventory item schema with common fields."""
    sku: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: ItemCategory
    brand: Optional[str] = Field(None, max_length=100)
    model: Optional[str] = Field(None, max_length=100)
    unit_price: Decimal = Field(..., gt=0)
    cost_price: Optional[Decimal] = Field(None, ge=0)
    quantity_in_stock: int = Field(0, ge=0)
    minimum_stock_level: int = Field(0, ge=0)
    maximum_stock_level: Optional[int] = Field(None, ge=0)
    reorder_point: int = Field(0, ge=0)
    unit_of_measure: str = Field("pieces", max_length=50)
    weight: Optional[Decimal] = Field(None, ge=0)
    dimensions: Optional[str] = Field(None, max_length=100)
    barcode: Optional[str] = Field(None, max_length=100)
    status: ItemStatus = ItemStatus.ACTIVE
    is_tracked: bool = True
    notes: Optional[str] = None
    supplier_id: Optional[int] = None


class InventoryItemCreate(InventoryItemBase):
    """Schema for creating a new inventory item."""
    pass


class InventoryItemUpdate(BaseModel):
    """Schema for updating inventory item information."""
    sku: Optional[str] = Field(None, min_length=1, max_length=100)
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[ItemCategory] = None
    brand: Optional[str] = Field(None, max_length=100)
    model: Optional[str] = Field(None, max_length=100)
    unit_price: Optional[Decimal] = Field(None, gt=0)
    cost_price: Optional[Decimal] = Field(None, ge=0)
    minimum_stock_level: Optional[int] = Field(None, ge=0)
    maximum_stock_level: Optional[int] = Field(None, ge=0)
    reorder_point: Optional[int] = Field(None, ge=0)
    unit_of_measure: Optional[str] = Field(None, max_length=50)
    weight: Optional[Decimal] = Field(None, ge=0)
    dimensions: Optional[str] = Field(None, max_length=100)
    barcode: Optional[str] = Field(None, max_length=100)
    status: Optional[ItemStatus] = None
    is_tracked: Optional[bool] = None
    notes: Optional[str] = None
    supplier_id: Optional[int] = None


class InventoryItem(InventoryItemBase):
    """Schema for inventory item response."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_low_stock: bool
    is_out_of_stock: bool
    
    class Config:
        from_attributes = True


class InventoryItemList(BaseModel):
    """Schema for paginated inventory item list response."""
    items: List[InventoryItem]
    total: int
    page: int
    size: int
    pages: int


class StockAdjustment(BaseModel):
    """Schema for stock adjustment operations."""
    item_id: int
    quantity_change: int
    reason: str = Field(..., min_length=1, max_length=255)
    reference_number: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class InventoryUpdate(BaseModel):
    """Schema for inventory update history."""
    id: int
    item_id: int
    user_id: int
    change_type: str
    quantity_change: int
    previous_quantity: int
    new_quantity: int
    reason: Optional[str] = None
    reference_number: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class LowStockAlert(BaseModel):
    """Schema for low stock alerts."""
    item_id: int
    sku: str
    name: str
    current_stock: int
    reorder_point: int
    minimum_stock_level: int
    supplier_name: Optional[str] = None
    
    class Config:
        from_attributes = True
