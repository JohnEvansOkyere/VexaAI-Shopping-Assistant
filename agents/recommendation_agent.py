from typing import List, Dict, Tuple, Any
import streamlit as st

class RecommendationAgent:
    def __init__(self):
        self.product_categories = {
            'smartphones': {
                'budget': [
                    {'title': 'Tecno Spark 8', 'price': 'GH₵ 800', 'specs': '4GB RAM, 64GB Storage'},
                    {'title': 'Infinix Hot 11', 'price': 'GH₵ 900', 'specs': '4GB RAM, 128GB Storage'},
                    {'title': 'Samsung Galaxy A12', 'price': 'GH₵ 1,200', 'specs': '4GB RAM, 128GB Storage'}
                ],
                'mid_range': [
                    {'title': 'Samsung Galaxy A52', 'price': 'GH₵ 2,500', 'specs': '6GB RAM, 128GB Storage'},
                    {'title': 'iPhone 11', 'price': 'GH₵ 3,800', 'specs': '4GB RAM, 128GB Storage'},
                    {'title': 'Xiaomi Redmi Note 11', 'price': 'GH₵ 2,200', 'specs': '6GB RAM, 128GB Storage'}
                ],
                'premium': [
                    {'title': 'Samsung Galaxy S21', 'price': 'GH₵ 5,500', 'specs': '8GB RAM, 256GB Storage'},
                    {'title': 'iPhone 13', 'price': 'GH₵ 6,800', 'specs': '6GB RAM, 128GB Storage'},
                    {'title': 'Google Pixel 6', 'price': 'GH₵ 4,500', 'specs': '8GB RAM, 128GB Storage'}
                ]
            },
            'laptops': {
                'budget': [
                    {'title': 'HP Pavilion 15', 'price': 'GH₵ 2,800', 'specs': 'Intel i3, 8GB RAM, 256GB SSD'},
                    {'title': 'Lenovo IdeaPad 3', 'price': 'GH₵ 3,200', 'specs': 'AMD Ryzen 5, 8GB RAM'},
                    {'title': 'Dell Inspiron 15', 'price': 'GH₵ 3,500', 'specs': 'Intel i5, 8GB RAM, 512GB SSD'}
                ],
                'mid_range': [
                    {'title': 'MacBook Air M1', 'price': 'GH₵ 6,500', 'specs': 'M1 Chip, 8GB RAM, 256GB SSD'},
                    {'title': 'HP Envy x360', 'price': 'GH₵ 5,200', 'specs': 'AMD Ryzen 7, 16GB RAM'},
                    {'title': 'Lenovo ThinkPad E15', 'price': 'GH₵ 4,800', 'specs': 'Intel i7, 16GB RAM'}
                ],
                'premium': [
                    {'title': 'MacBook Pro 14"', 'price': 'GH₵ 12,000', 'specs': 'M1 Pro, 16GB RAM, 512GB SSD'},
                    {'title': 'Dell XPS 13', 'price': 'GH₵ 8,500', 'specs': 'Intel i7, 16GB RAM, 1TB SSD'},
                    {'title': 'HP Spectre x360', 'price': 'GH₵ 9,200', 'specs': 'Intel i7, 16GB RAM, 512GB SSD'}
                ]
            }
        }
        
        self.trending_products = [
            {'title': 'AirPods Pro 2nd Gen', 'price': 'GH₵ 1,800', 'category': 'Audio'},
            {'title': 'Samsung Galaxy Watch 4', 'price': 'GH₵ 1,200', 'category': 'Wearables'},
            {'title': 'iPad Air 5th Gen', 'price': 'GH₵ 4,500', 'category': 'Tablets'},
            {'title': 'Sony WH-1000XM4', 'price': 'GH₵ 2,200', 'category': 'Headphones'},
            {'title': 'Nintendo Switch OLED', 'price': 'GH₵ 2,800', 'category': 'Gaming'}
        ]
    
    def determine_budget_category(self, budget: Dict[str, int]) -> str:
        """Determine budget category based on price range"""
        if not budget:
            return 'mid_range'
        
        max_budget = budget.get('max', budget.get('min', 0))
        
        if max_budget <= 1500:
            return 'budget'
        elif max_budget <= 5000:
            return 'mid_range'
        else:
            return 'premium'
    
    def get_category_from_query(self, query: str) -> str:
        """Determine product category from query"""
        query_lower = query.lower()
        
        phone_keywords = ['phone', 'smartphone', 'mobile', 'iphone', 'samsung', 'galaxy', 'android']
        laptop_keywords = ['laptop', 'computer', 'macbook', 'notebook', 'pc']
        
        if any(keyword in query_lower for keyword in phone_keywords):
            return 'smartphones'
        elif any(keyword in query_lower for keyword in laptop_keywords):
            return 'laptops'
        
        return 'smartphones'  # Default
    
    def format_recommendations(self, products: List[Dict], category: str, budget_category: str) -> List[Dict[str, str]]:
        """Format recommendations as product cards"""
        formatted_products = []
        
        for product in products:
            formatted_product = {
                'title': product['title'],
                'price': product['price'],
                'location': 'Accra, Greater Accra',  # Default location
                'link': f"https://jiji.com.gh/search?query={product['title'].replace(' ', '+')}"
            }
            formatted_products.append(formatted_product)
        
        return formatted_products
    
    def get_recommendations(self, query: str, entities: Dict[str, Any]) -> Tuple[str, List[Dict[str, str]]]:
        """Generate product recommendations"""
        category = self.get_category_from_query(query)
        budget_category = self.determine_budget_category(entities.get('budget', {}))
        
        # Get recommendations based on category and budget
        if category in self.product_categories:
            recommendations = self.product_categories[category].get(budget_category, [])
        else:
            recommendations = self.trending_products[:5]
        
        if not recommendations:
            response = """
            **Product Recommendations**
            
            I'd love to give you personalized recommendations! Could you tell me:
            • What type of product you're looking for?
            • Your budget range?
            • Any specific features you need?
            
            **Popular Categories:**
            • Smartphones & Tablets
            • Laptops & Computers  
            • Audio & Headphones
            • Gaming & Entertainment
            • Cars & Vehicles
            """
            return response, []
        
        # Format products for display
        products = self.format_recommendations(recommendations, category, budget_category)
        
        budget_text = ""
        if entities.get('budget'):
            budget = entities['budget']
            if 'min' in budget and 'max' in budget:
                budget_text = f" within your GHS {budget['min']:,} - GHS {budget['max']:,} budget"
            elif 'max' in budget:
                budget_text = f" under GHS {budget['max']:,}"
        
        response = f"""
        **Recommended {category.title()}** {budget_text}
        
        Based on your preferences, here are my top recommendations:
        
        These products offer great value for money and are popular choices in Ghana!
        """
        
        # Store in session state
        st.session_state.current_products = products
        
        return response, products
    
    def get_trending_products(self) -> Tuple[str, List[Dict[str, str]]]:
        """Get trending products"""
        products = self.format_recommendations(self.trending_products, 'trending', 'mixed')
        
        response = """
        **Trending Products Right Now** 🔥
        
        Here are the most popular items on Jiji.com.gh:
        """
        
        return response, products
    
    def get_personalized_recommendations(self, user_preferences: Dict[str, Any]) -> str:
        """Generate personalized recommendations based on user history"""
        return """
        **Personalized Recommendations** (Coming Soon!)
        
        Soon I'll provide recommendations based on:
        • Your previous searches and purchases
        • Items you've viewed and saved
        • Your budget preferences
        • Popular items in your area
        • Seasonal trends and deals
        
        **For now, try:**
        • "Recommend smartphones under GHS 3000"
        • "Best laptops for students"
        • "Popular headphones in Ghana"
        """