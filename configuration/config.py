# Configuration file for AI Shopping Assistant

# Application Settings
APP_CONFIG = {
    'title': '🛍️ AI Shopping Assistant',
    'subtitle': 'Your intelligent shopping companion for Jiji.com.gh',
    'page_icon': '🛍️',
    'layout': 'wide'
}

# Jiji.com.gh Settings
JIJI_CONFIG = {
    'base_url': 'https://jiji.com.gh',
    'search_endpoint': '/search',
    'max_results': 10,
    'request_timeout': 10,
    'retry_attempts': 3
}

# Web Scraping Settings
SCRAPING_CONFIG = {
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    },
    'delay_between_requests': 1,  # seconds
    'max_retries': 3
}

# Product Categories Configuration
PRODUCT_CATEGORIES = {
    'electronics': {
        'smartphones': ['phone', 'smartphone', 'mobile', 'iphone', 'samsung', 'galaxy', 'android', 'ios'],
        'laptops': ['laptop', 'computer', 'macbook', 'notebook', 'pc', 'gaming laptop'],
        'tablets': ['tablet', 'ipad', 'android tablet', 'tab'],
        'audio': ['headphone', 'earphone', 'speaker', 'airpods', 'bluetooth'],
        'cameras': ['camera', 'dslr', 'gopro', 'camcorder'],
        'gaming': ['playstation', 'xbox', 'nintendo', 'gaming console', 'ps5', 'ps4'],
        'accessories': ['charger', 'cable', 'case', 'screen protector', 'power bank']
    },
    'vehicles': {
        'cars': ['car', 'vehicle', 'auto', 'sedan', 'suv', 'truck'],
        'motorcycles': ['motorcycle', 'bike', 'motorbike', 'scooter'],
        'parts': ['spare parts', 'car parts', 'auto parts', 'tires', 'battery']
    },
    'home': {
        'furniture': ['furniture', 'chair', 'table', 'bed', 'sofa', 'wardrobe'],
        'appliances': ['refrigerator', 'washing machine', 'microwave', 'air conditioner'],
        'decor': ['decoration', 'art', 'lamp', 'mirror', 'curtain']
    }
}

# Budget Categories
BUDGET_RANGES = {
    'budget': {'min': 0, 'max': 1500},
    'mid_range': {'min': 1500, 'max': 5000},
    'premium': {'min': 5000, 'max': float('inf')}
}

# Ghana Cities for Location Filtering
GHANA_CITIES = [
    'Accra', 'Kumasi', 'Tamale', 'Cape Coast', 'Tema', 'Sekondi-Takoradi',
    'Koforidua', 'Ho', 'Wa', 'Sunyani', 'Techiman', 'Obuasi', 'Tarkwa',
    'Bolgatanga', 'Takoradi', 'Nkawkaw', 'Yendi', 'Kintampo'
]

# UI Configuration
UI_CONFIG = {
    'primary_color': '#1976d2',
    'secondary_color': '#2e7d32',
    'background_color': '#f5f5f5',
    'text_color': '#333333',
    'max_chat_messages': 100,
    'products_per_page': 10
}

# Chat Responses
DEFAULT_RESPONSES = {
    'welcome': """
    Hello! I'm your AI shopping assistant for Jiji.com.gh. I can help you:
    
    • 🔍 **Find Products** - Search within your budget
    • 📦 **Track Orders** - Monitor delivery status  
    • ❓ **Answer Questions** - FAQ and support
    • 💡 **Recommendations** - Personalized suggestions
    • ⚖️ **Compare Items** - Side-by-side comparisons
    • 🔔 **Price Alerts** - Get notified of deals
    
    What are you looking for today?
    """,
    
    'no_products_found': """
    Sorry, I couldn't find any products matching your request.
    
    **Try:**
    • Different keywords
    • Broader search terms
    • Adjusting your budget range
    • Checking spelling
    """,
    
    'search_error': """
    I encountered an issue while searching. Please try again or visit Jiji.com.gh directly.
    """,
    
    'unknown_intent': """
    I'm not sure how to help with that. Try asking about:
    • Product searches
    • Order tracking  
    • Payment questions
    • Shipping information
    """
}

# Feature Flags
FEATURES = {
    'enable_scraping': True,
    'enable_order_tracking': True,
    'enable_recommendations': True,
    'enable_price_alerts': False,  # Coming soon
    'enable_comparison': False,    # Coming soon
    'enable_favorites': False,     # Coming soon
    'enable_user_accounts': False  # Future feature
}

# API Configuration (for future integrations)
API_CONFIG = {
    'jiji_api_base': 'https://api.jiji.com.gh',  # Hypothetical
    'rate_limit': 100,  # requests per hour
    'cache_duration': 300  # seconds
}