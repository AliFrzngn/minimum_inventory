"""
Inventory item model for managing stock and product information.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Numeric, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class ItemCategory(str, enum.Enum):
    """Inventory item categories."""
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    BOOKS = "books"
    TOOLS = "tools"
    FURNITURE = "furniture"
    OTHER = "other"


class ItemStatus(str, enum.Enum):
    """Inventory item status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"


class InventoryItem(Base):
    """Inventory item model for managing products and stock."""
    
    __tablename__ = "inventory_items"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    category = Column(Enum(ItemCategory), nullable=False)
    brand = Column(String(100))
    model = Column(String(100))
    unit_price = Column(Numeric(10, 2), nullable=False)
    cost_price = Column(Numeric(10, 2))
    quantity_in_stock = Column(Integer, default=0, nullable=False)
    minimum_stock_level = Column(Integer, default=0, nullable=False)
    maximum_stock_level = Column(Integer)
    reorder_point = Column(Integer, default=0, nullable=False)
    unit_of_measure = Column(String(50), default="pieces")
    weight = Column(Numeric(8, 3))  # in kg
    dimensions = Column(String(100))  # e.g., "10x20x30 cm"
    barcode = Column(String(100), unique=True, index=True)
    status = Column(Enum(ItemStatus), default=ItemStatus.ACTIVE, nullable=False)
    is_tracked = Column(Boolean, default=True, nullable=False)  # Whether to track stock levels
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    
    # Relationships
    supplier = relationship("Supplier", back_populates="items")
    order_items = relationship("OrderItem", back_populates="item")
    inventory_updates = relationship("InventoryUpdate", back_populates="item")
    
    def __repr__(self):
        return f"<InventoryItem(id={self.id}, sku='{self.sku}', name='{self.name}')>"
    
    @property
    def is_low_stock(self) -> bool:
        """Check if item is below reorder point."""
        return self.quantity_in_stock <= self.reorder_point
    
    @property
    def is_out_of_stock(self) -> bool:
        """Check if item is out of stock."""
        return self.quantity_in_stock <= 0


class InventoryUpdate(Base):
    """Model for tracking inventory changes and stock movements."""
    
    __tablename__ = "inventory_updates"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    change_type = Column(String(50), nullable=False)  # "in", "out", "adjustment", "return"
    quantity_change = Column(Integer, nullable=False)  # Positive for increase, negative for decrease
    previous_quantity = Column(Integer, nullable=False)
    new_quantity = Column(Integer, nullable=False)
    reason = Column(String(255))
    reference_number = Column(String(100))  # Order number, PO number, etc.
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    item = relationship("InventoryItem", back_populates="inventory_updates")
    user = relationship("User", back_populates="inventory_updates")
    
    def __repr__(self):
        return f"<InventoryUpdate(id={self.id}, item_id={self.item_id}, change={self.quantity_change})>"
