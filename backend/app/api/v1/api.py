"""
Main API router that includes all endpoint routers.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, inventory, suppliers, orders, users

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
