"""
Order models for managing purchase orders and sales orders.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Numeric, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class OrderType(str, enum.Enum):
    """Order types."""
    PURCHASE = "purchase"  # Incoming stock
    SALE = "sale"  # Outgoing stock
    TRANSFER = "transfer"  # Internal transfer
    RETURN = "return"  # Return to supplier


class OrderStatus(str, enum.Enum):
    """Order status."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"


class Order(Base):
    """Order model for managing purchase and sales orders."""
    
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), unique=True, index=True, nullable=False)
    order_type = Column(Enum(OrderType), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    
    # Order details
    total_amount = Column(Numeric(15, 2), default=0, nullable=False)
    tax_amount = Column(Numeric(15, 2), default=0, nullable=False)
    discount_amount = Column(Numeric(15, 2), default=0, nullable=False)
    shipping_cost = Column(Numeric(10, 2), default=0, nullable=False)
    
    # Dates
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    expected_delivery_date = Column(DateTime(timezone=True))
    actual_delivery_date = Column(DateTime(timezone=True))
    
    # Shipping information
    shipping_address = Column(Text)
    shipping_city = Column(String(100))
    shipping_state = Column(String(100))
    shipping_country = Column(String(100))
    shipping_postal_code = Column(String(20))
    
    # Additional information
    notes = Column(Text)
    internal_notes = Column(Text)
    tracking_number = Column(String(100))
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="orders")
    supplier = relationship("Supplier", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order(id={self.id}, order_number='{self.order_number}', type='{self.order_type}')>"


class OrderItem(Base):
    """Order item model for individual items within an order."""
    
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(15, 2), nullable=False)
    notes = Column(Text)
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    item = relationship("InventoryItem", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, item_id={self.item_id}, qty={self.quantity})>"
