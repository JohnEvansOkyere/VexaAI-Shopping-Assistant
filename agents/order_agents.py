from typing import Dict, Any
import re
import random

class OrderAgent:
    def __init__(self):
        self.order_statuses = [
            "Order Confirmed",
            "Processing",
            "Shipped",
            "Out for Delivery",
            "Delivered"
        ]
    
    def extract_order_number(self, text: str) -> str:
        """Extract order number from user input"""
        # Look for patterns like: JJ123456, order 123456, #123456
        patterns = [
            r'(?:order\s*(?:number)?[:#\s]*)?([A-Z]{2}\d{6})',
            r'(?:order\s*(?:number)?[:#\s]*)(\d{6,8})',
            r'#(\w+)',
            r'order\s+(\w+)'
        ]
        
        text_upper = text.upper()
        for pattern in patterns:
            match = re.search(pattern, text_upper)
            if match:
                return match.group(1)
        
        return None
    
    def generate_sample_tracking_info(self, order_number: str) -> Dict[str, Any]:
        """Generate sample tracking information"""
        # Simulate order tracking (replace with real API integration)
        status_index = hash(order_number) % len(self.order_statuses)
        current_status = self.order_statuses[status_index]
        
        tracking_info = {
            'order_number': order_number,
            'status': current_status,
            'estimated_delivery': "2-3 business days",
            'last_update': "Today, 2:30 PM",
            'tracking_details': [
                {"time": "Today, 2:30 PM", "status": current_status, "location": "Accra Sorting Facility"},
                {"time": "Yesterday, 4:15 PM", "status": "Shipped", "location": "Kumasi Warehouse"},
                {"time": "2 days ago, 10:00 AM", "status": "Processing", "location": "Seller Location"}
            ]
        }
        
        return tracking_info
    
    def track_order(self, query: str, entities: Dict[str, Any]) -> str:
        """Handle order tracking requests"""
        order_number = self.extract_order_number(query)
        
        if not order_number:
            return """
            **Order Tracking**
            
            I'd be happy to help track your order! Please provide your order number.
            
            **Examples:**
            • "Track order JJ123456"
            • "Where is my order #123456"
            • "Order status for 123456"
            
            **Note:** Order tracking is currently in development. Full integration with Jiji's tracking system coming soon!
            """
        
        # Generate sample tracking info
        tracking_info = self.generate_sample_tracking_info(order_number)
        
        response = f"""
        **Order Tracking - #{tracking_info['order_number']}**
        
        **Current Status:** 🚚 {tracking_info['status']}
        **Last Update:** {tracking_info['last_update']}
        **Estimated Delivery:** {tracking_info['estimated_delivery']}
        
        **Tracking History:**
        """
        
        for update in tracking_info['tracking_details']:
            status_emoji = self.get_status_emoji(update['status'])
            response += f"\n• {status_emoji} **{update['status']}** - {update['time']} ({update['location']})"
        
        response += """
        
        **Need Help?**
        Contact the seller directly through Jiji or reach out to Jiji support if you have concerns about your order.
        
        *Note: This is a demo tracking system. Real integration coming soon!*
        """
        
        return response
    
    def get_status_emoji(self, status: str) -> str:
        """Get emoji for order status"""
        emoji_map = {
            "Order Confirmed": "✅",
            "Processing": "⏳",
            "Shipped": "📦",
            "Out for Delivery": "🚚",
            "Delivered": "🎉"
        }
        return emoji_map.get(status, "📋")
    
    def get_order_history(self, user_id: str = None) -> str:
        """Get user's order history (placeholder)"""
        return """
        **Order History** (Coming Soon!)
        
        Soon you'll be able to:
        • View all your past orders
        • Track multiple orders at once
        • Reorder favorite items
        • Download order receipts
        
        **Current Orders:**
        • Order #JJ123456 - Samsung Galaxy S20 - Shipped
        • Order #JJ123457 - iPhone 13 Pro - Processing
        
        *Full order management system in development!*
        """