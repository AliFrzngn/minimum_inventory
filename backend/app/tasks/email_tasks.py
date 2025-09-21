"""
Email-related background tasks.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
from celery import current_task

from app.core.celery_app import celery_app
from app.core.config import settings


@celery_app.task(bind=True)
def send_low_stock_alert(self, alert_data: Dict[str, Any]):
    """Send low stock alert email to managers."""
    try:
        # Update task status
        current_task.update_state(
            state="PROGRESS",
            meta={"message": "Preparing low stock alert email"}
        )
        
        # Create email content
        subject = f"Low Stock Alert: {alert_data['item_name']}"
        body = f"""
        Low Stock Alert
        
        Item: {alert_data['item_name']}
        SKU: {alert_data['sku']}
        Current Stock: {alert_data['current_stock']}
        Reorder Point: {alert_data['reorder_point']}
        Minimum Stock Level: {alert_data['minimum_stock_level']}
        Supplier: {alert_data.get('supplier_name', 'N/A')}
        
        Please reorder this item as soon as possible.
        """
        
        # Send email if SMTP is configured
        if settings.SMTP_HOST:
            send_email(
                to=settings.SMTP_USER,
                subject=subject,
                body=body
            )
        
        return {"status": "success", "message": "Low stock alert sent"}
        
    except Exception as exc:
        # Update task state with error
        current_task.update_state(
            state="FAILURE",
            meta={"error": str(exc)}
        )
        raise


@celery_app.task(bind=True)
def send_order_notification(self, order_data: Dict[str, Any], notification_type: str):
    """Send order-related notification emails."""
    try:
        current_task.update_state(
            state="PROGRESS",
            meta={"message": f"Preparing {notification_type} notification"}
        )
        
        if notification_type == "order_created":
            subject = f"New Order Created: {order_data['order_number']}"
            body = f"""
            A new order has been created.
            
            Order Number: {order_data['order_number']}
            Order Type: {order_data['order_type']}
            Total Amount: ${order_data['total_amount']}
            Created By: {order_data['created_by']}
            """
        elif notification_type == "order_delivered":
            subject = f"Order Delivered: {order_data['order_number']}"
            body = f"""
            Order has been delivered.
            
            Order Number: {order_data['order_number']}
            Delivered On: {order_data['delivery_date']}
            """
        else:
            return {"status": "error", "message": "Unknown notification type"}
        
        if settings.SMTP_HOST:
            send_email(
                to=settings.SMTP_USER,
                subject=subject,
                body=body
            )
        
        return {"status": "success", "message": f"{notification_type} notification sent"}
        
    except Exception as exc:
        current_task.update_state(
            state="FAILURE",
            meta={"error": str(exc)}
        )
        raise


def send_email(to: str, subject: str, body: str):
    """Send email using SMTP."""
    if not settings.SMTP_HOST:
        return
    
    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_USER
    msg["To"] = to
    msg["Subject"] = subject
    
    msg.attach(MIMEText(body, "plain"))
    
    server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
    if settings.SMTP_TLS:
        server.starttls()
    
    if settings.SMTP_USER and settings.SMTP_PASSWORD:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    
    text = msg.as_string()
    server.sendmail(settings.SMTP_USER, to, text)
    server.quit()
