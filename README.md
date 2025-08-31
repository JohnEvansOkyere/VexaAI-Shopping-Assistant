# VexaAI-Shopping-Assistant

# 🛍️ AI Shopping Assistant for Jiji.com.gh

A chat-based AI shopping assistant built with Streamlit that helps users find products on Jiji.com.gh through natural language conversations.

## Features

### 🤖 Intelligent Agent Capabilities
- **Product Search** - Search Jiji.com.gh with natural language queries
- **Order Tracking** - Track order status (placeholder with demo data)
- **FAQ Support** - Answer common shopping questions
- **Product Recommendations** - Get personalized product suggestions
- **Product Comparison** - Compare different products (coming soon)
- **Price Alerts** - Set alerts for price drops (coming soon)

### 💬 Chat Interface
- Real-time chat with conversation history
- Product cards with clickable links
- Budget filtering and constraints
- Smart intent detection
- Error handling and fallbacks

### 🎯 Smart Features
- Natural language processing for user queries
- Budget range extraction and filtering
- Location-based results
- Product specification parsing
- Session management and user preferences

## Installation

### 1. Create Project Structure
```bash
mkdir ai-shopping-assistant
cd ai-shopping-assistant

# Create directories
mkdir agents utils

# Create empty __init__.py files
touch agents/__init__.py
touch utils/__init__.py
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. File Structure
```
ai-shopping-assistant/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                      # This file
├── agents/
│   ├── __init__.py
│   ├── intent_classifier.py       # Intent classification logic
│   ├── product_agent.py          # Product search and scraping
│   ├── order_agent.py            # Order tracking functionality
│   ├── faq_agent.py              # FAQ and support handling
│   └── recommendation_agent.py    # Product recommendations
└── utils/
    ├── __init__.py
    └── session_manager.py         # Session state management
```

## Usage

### 1. Run the Application
```bash
streamlit run app.py
```

### 2. Example Interactions

**Product Search:**
- "I want to buy Samsung S20 Ultra, 120GB, budget GHS3000–5000"
- "Find iPhone 13 under GHS 4000"
- "Looking for gaming laptops between GHS 2000-5000"
- "Bluetooth headphones in Accra"

**Order Tracking:**
- "Track order JJ123456"
- "Where is my order #123456"
- "Order status for 789012"

**FAQ & Support:**
- "How do I pay on Jiji?"
- "Is Jiji safe to use?"
- "What are the return policies?"
- "How to create an account?"

**Recommendations:**
- "Recommend good smartphones"
- "Best laptops for students"
- "Popular headphones under GHS 1000"

## Features Breakdown

### Intent Classification
The system automatically detects user intent from natural language:
- Product searches with budget constraints
- Order tracking requests
- FAQ and support questions
- Recommendation requests
- Product comparisons
- Price alert setups

### Product Search
- Scrapes live data from Jiji.com.gh
- Filters by budget, location, and specifications
- Returns top 10 relevant results
- Handles various product categories
- Error handling with fallback sample data

### Smart Budget Processing
- Extracts budget ranges from natural language
- Supports formats like "under GHS 3000", "between 2000-5000"
- Filters search results automatically
- Shows budget statistics in sidebar

### Session Management
- Persistent chat history
- User preferences tracking
- Search history
- Favorite products (coming soon)
- Session statistics

## Customization

### Adding New Intents
1. Add patterns to `intent_classifier.py`
2. Create new agent class in `agents/` directory
3. Add routing logic in `app.py`

### Modifying Scraping Logic
- Update `product_agent.py` for different websites
- Modify CSS selectors for different page structures
- Add new product categories and parsing rules

### Extending Recommendations
- Add more product categories in `recommendation_agent.py`
- Implement ML-based recommendations
- Add user behavior tracking

## Technical Notes

### Web Scraping
- Uses BeautifulSoup4 for HTML parsing
- Implements multiple fallback CSS selectors
- Handles rate limiting and errors gracefully
- Respects robots.txt and site policies

### Error Handling
- Comprehensive try-catch blocks
- Fallback sample data when scraping fails
- User-friendly error messages
- Graceful degradation of features

### Performance
- Session-based caching
- Efficient DOM parsing
- Minimal external requests
- Responsive UI with loading indicators

## Future Enhancements

### Phase 1 (Next Updates)
- [ ] Real-time price alerts
- [ ] Product comparison tables
- [ ] User accounts and saved searches
- [ ] Email notifications

### Phase 2 (Advanced Features)
- [ ] Machine learning recommendations
- [ ] Image-based product search
- [ ] Multi-vendor price comparison
- [ ] Advanced filtering options

### Phase 3 (Full Platform)
- [ ] Order management integration
- [ ] Seller communication tools
- [ ] Payment gateway integration
- [ ] Mobile app companion

## Support

For issues or feature requests:
1. Check existing functionality in the chat interface
2. Try different query phrasings
3. Use the sidebar quick actions
4. Clear chat history if experiencing issues

## Contributing

This is a modular system designed for easy extension:
- Add new agents in the `agents/` directory
- Extend intent classification patterns
- Improve scraping reliability
- Add new product categories
- Enhance UI/UX components

---

**Built with ❤️ for Ghana's e-commerce community**