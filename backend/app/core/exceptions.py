"""
Custom exception handlers for the FastAPI application.
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)


class InventoryException(Exception):
    """Base exception for inventory-related errors."""
    pass


class InsufficientStockException(InventoryException):
    """Raised when there's insufficient stock for an operation."""
    pass


class ItemNotFoundException(InventoryException):
    """Raised when an inventory item is not found."""
    pass


class SupplierNotFoundException(InventoryException):
    """Raised when a supplier is not found."""
    pass


class OrderNotFoundException(InventoryException):
    """Raised when an order is not found."""
    pass


class AuthenticationException(InventoryException):
    """Raised when authentication fails."""
    pass


class AuthorizationException(InventoryException):
    """Raised when authorization fails."""
    pass


def setup_exception_handlers(app):
    """Setup custom exception handlers for the FastAPI app."""
    
    @app.exception_handler(InventoryException)
    async def inventory_exception_handler(request: Request, exc: InventoryException):
        """Handle custom inventory exceptions."""
        logger.error(f"Inventory exception: {exc}")
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc), "type": exc.__class__.__name__}
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "type": "HTTPException"}
        )
    
    @app.exception_handler(StarletteHTTPException)
    async def starlette_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle Starlette HTTP exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "type": "StarletteHTTPException"}
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle request validation errors."""
        return JSONResponse(
            status_code=422,
            content={
                "detail": "Validation error",
                "errors": exc.errors(),
                "type": "ValidationError"
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions."""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "type": "InternalServerError"
            }
        )
