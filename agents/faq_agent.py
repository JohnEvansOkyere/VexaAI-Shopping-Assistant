from typing import Dict, Any
import re

class FAQAgent:
    def __init__(self):
        self.faq_database = {
            'payment': {
                'keywords': ['payment', 'pay', 'money', 'cash', 'card', 'mobile money', 'momo'],
                'response': """
                **Payment Options on Jiji.com.gh:**
                
                • **Mobile Money** - MTN Mobile Money, AirtelTigo Money, Vodafone Cash
                • **Bank Transfer** - Direct bank transfers to seller accounts
                • **Cash on Delivery** - Pay when item is delivered (where available)
                • **Credit/Debit Cards** - Visa, Mastercard accepted
                
                **Safety Tips:**
                • Always use Jiji's secure payment system
                • Avoid sending money before seeing the item
                • Use escrow services for high-value items
                """
            },
            'shipping': {
                'keywords': ['shipping', 'delivery', 'transport', 'courier', 'send'],
                'response': """
                **Shipping & Delivery:**
                
                • **Seller Arranged** - Most sellers arrange their own delivery
                • **Pickup Available** - Meet sellers in safe, public locations
                • **Courier Services** - Professional courier companies available
                • **Delivery Time** - Usually 1-5 business days within Ghana
                
                **Delivery Locations:**
                • All major cities: Accra, Kumasi, Tamale, Cape Coast
                • Rural areas may have additional charges
                """
            },
            'returns': {
                'keywords': ['return', 'refund', 'exchange', 'warranty', 'guarantee'],
                'response': """
                **Returns & Refunds:**
                
                • **Return Policy** - Varies by seller (check individual listings)
                • **Condition** - Items must be in original condition
                • **Timeframe** - Usually 7-14 days from delivery
                • **Process** - Contact seller first, then Jiji support if needed
                
                **Protection:**
                • Jiji Buyer Protection available on eligible items
                • Report issues through the platform
                • Keep all communication on Jiji for protection
                """
            },
            'safety': {
                'keywords': ['safe', 'security', 'scam', 'fraud', 'trust', 'legitimate'],
                'response': """
                **Shopping Safely on Jiji:**
                
                **Red Flags to Avoid:**
                • Prices too good to be true
                • Sellers asking for payment outside Jiji
                • No phone verification or reviews
                • Pressure to complete transaction quickly
                
                **Safety Tips:**
                • Check seller ratings and reviews
                • Use Jiji's messaging system
                • Meet in public places for pickup
                • Inspect items before payment
                • Use secure payment methods
                """
            },
            'account': {
                'keywords': ['account', 'profile', 'login', 'register', 'sign up', 'password'],
                'response': """
                **Account Management:**
                
                **Creating Account:**
                • Visit jiji.com.gh and click "Register"
                • Verify your phone number
                • Add profile information
                
                **Account Features:**
                • Save favorite items
                • Track your orders
                • Manage listings (if selling)
                • View purchase history
                • Update personal information
                
                **Forgot Password:** Use the "Forgot Password" link on login page
                """
            }
        }
    
    def find_best_match(self, query: str) -> str:
        """Find the best FAQ match for user query"""
        query_lower = query.lower()
        best_match = None
        max_matches = 0
        
        for category, data in self.faq_database.items():
            matches = sum(1 for keyword in data['keywords'] if keyword in query_lower)
            if matches > max_matches:
                max_matches = matches
                best_match = category
        
        return best_match if max_matches > 0 else None
    
    def handle_inquiry(self, query: str, entities: Dict[str, Any]) -> str:
        """Handle FAQ and support inquiries"""
        # Find best matching FAQ
        best_match = self.find_best_match(query)
        
        if best_match:
            return self.faq_database[best_match]['response']
        
        # Handle specific questions
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['how', 'what', 'why', 'when', 'where']):
            if 'jiji' in query_lower:
                return """
                **About Jiji.com.gh:**
                
                Jiji is Ghana's largest online marketplace where you can:
                • Buy and sell almost anything
                • Find great deals from verified sellers
                • Shop safely with buyer protection
                • Connect with local sellers
                
                **Popular Categories:**
                • Mobile Phones & Tablets
                • Cars & Vehicles
                • Electronics & Computers
                • Fashion & Beauty
                • Home & Furniture
                """
            
            elif any(word in query_lower for word in ['work', 'use', 'buy']):
                return """
                **How to Buy on Jiji:**
                
                1. **Search** - Use the search bar or browse categories
                2. **Filter** - Set your budget, location, and preferences
                3. **Contact** - Message the seller through Jiji
                4. **Negotiate** - Discuss price and delivery
                5. **Pay Safely** - Use Jiji's secure payment options
                6. **Receive** - Get your item delivered or arrange pickup
                
                **Tips for Better Results:**
                • Be specific in your search terms
                • Check seller ratings before buying
                • Ask questions about the product condition
                • Negotiate respectfully
                """
        
        # Default response for unmatched queries
        return """
        **I'm here to help!** 
        
        I can assist you with:
        • **Product searches** - Find items on Jiji.com.gh
        • **Payment information** - Learn about payment options
        • **Shipping details** - Understand delivery processes  
        • **Safety tips** - Shop securely and avoid scams
        • **Returns & refunds** - Know your rights as a buyer
        • **Account help** - Manage your Jiji account
        
        **Need specific help?** Try asking:
        • "How do I pay on Jiji?"
        • "Is Jiji safe to use?"
        • "How do returns work?"
        • "How to create an account?"
        
        **Or search for products:** "Find Samsung phones under GHS 2000"
        """
    
    def get_contact_info(self) -> str:
        """Provide Jiji contact information"""
        return """
        **Contact Jiji Support:**
        
        • **Website:** [jiji.com.gh](https://jiji.com.gh)
        • **Help Center:** Available on the website
        • **Phone:** Check website for current contact numbers
        • **Email:** Support available through the platform
        
        **For Urgent Issues:**
        • Use the "Report" button on problematic listings
        • Contact customer service through your account
        • Use the live chat feature on the website
        """