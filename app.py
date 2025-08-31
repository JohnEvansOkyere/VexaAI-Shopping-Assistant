import streamlit as st
import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

from agents.intent_classifier import IntentClassifier
from agents.product_agent import ProductAgent
from agents.order_agent import OrderAgent
from agents.faq_agent import FAQAgent
from agents.recommendation_agent import RecommendationAgent
from utils.session_manager import SessionManager

# Page configuration
st.set_page_config(
    page_title="AI Shopping Assistant",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better chat UI
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    .bot-message {
        background-color: #f5f5f5;
        margin-right: 20%;
    }
    .product-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .product-title {
        font-weight: bold;
        color: #1976d2;
        margin-bottom: 0.5rem;
    }
    .product-price {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2e7d32;
    }
    .product-location {
        color: #666;
        font-size: 0.9rem;
    }
    .sidebar-content {
        padding: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class ShoppingAssistant:
    def __init__(self):
        self.session_manager = SessionManager()
        self.intent_classifier = IntentClassifier()
        self.product_agent = ProductAgent()
        self.order_agent = OrderAgent()
        self.faq_agent = FAQAgent()
        self.recommendation_agent = RecommendationAgent()
        
    def initialize_session(self):
        """Initialize session state variables"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'user_preferences' not in st.session_state:
            st.session_state.user_preferences = {}
        if 'current_products' not in st.session_state:
            st.session_state.current_products = []
    
    def display_chat_history(self):
        """Display chat history in a conversational format"""
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {message['content']}
                    <small style="color: #666;">{message['timestamp']}</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>🛍️ Assistant:</strong> {message['content']}
                    <small style="color: #666;">{message['timestamp']}</small>
                </div>
                """, unsafe_allow_html=True)
                
                # Display products if any
                if 'products' in message and message['products']:
                    self.display_products(message['products'])
    
    def display_products(self, products):
        """Display products in card format"""
        for i, product in enumerate(products):
            st.markdown(f"""
            <div class="product-card">
                <div class="product-title">{product.get('title', 'Product')}</div>
                <div class="product-price">{product.get('price', 'Price not available')}</div>
                <div class="product-location">📍 {product.get('location', 'Location not specified')}</div>
                <div style="margin-top: 0.5rem;">
                    <a href="{product.get('link', '#')}" target="_blank" 
                       style="background-color: #1976d2; color: white; padding: 0.5rem 1rem; 
                              text-decoration: none; border-radius: 4px; display: inline-block;">
                        View Product
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def add_to_chat_history(self, role, content, products=None):
        """Add message to chat history"""
        timestamp = datetime.now().strftime("%H:%M")
        message = {
            'role': role,
            'content': content,
            'timestamp': timestamp
        }
        if products:
            message['products'] = products
        st.session_state.chat_history.append(message)
    
    def process_user_message(self, user_input):
        """Process user input and generate response"""
        # Add user message to history
        self.add_to_chat_history('user', user_input)
        
        # Classify intent
        intent_result = self.intent_classifier.classify_intent(user_input)
        intent = intent_result['intent']
        entities = intent_result['entities']
        
        # Route to appropriate agent
        if intent == 'search_product':
            response, products = self.product_agent.search_products(user_input, entities)
            self.add_to_chat_history('assistant', response, products)
            
        elif intent == 'track_order':
            response = self.order_agent.track_order(user_input, entities)
            self.add_to_chat_history('assistant', response)
            
        elif intent == 'faq_inquiry':
            response = self.faq_agent.handle_inquiry(user_input, entities)
            self.add_to_chat_history('assistant', response)
            
        elif intent == 'get_recommendations':
            response, products = self.recommendation_agent.get_recommendations(user_input, entities)
            self.add_to_chat_history('assistant', response, products)
            
        elif intent == 'compare_products':
            response = self.product_agent.compare_products(user_input, entities)
            self.add_to_chat_history('assistant', response)
            
        elif intent == 'price_alert':
            response = self.product_agent.set_price_alert(user_input, entities)
            self.add_to_chat_history('assistant', response)
            
        else:
            # Default response for unrecognized intents
            response = """
            I'm here to help you with:
            • 🔍 **Product Search** - Find products on Jiji.com.gh
            • 📦 **Order Tracking** - Track your orders (coming soon)
            • ❓ **FAQ & Support** - Get answers to common questions
            • 💡 **Recommendations** - Get personalized product suggestions
            • ⚖️ **Product Comparison** - Compare different products
            • 🔔 **Price Alerts** - Set alerts for price drops
            
            Try asking something like: *"Find Samsung Galaxy phones under GHS 2000"*
            """
            self.add_to_chat_history('assistant', response)
    
    def render_sidebar(self):
        """Render sidebar with additional features"""
        st.sidebar.title("🛍️ Shopping Assistant")
        
        st.sidebar.markdown("### Quick Actions")
        
        # Popular searches
        st.sidebar.markdown("**Popular Searches:**")
        popular_searches = [
            "Samsung Galaxy phones",
            "iPhone under GHS 3000",
            "Gaming laptops",
            "Bluetooth headphones",
            "Android tablets"
        ]
        
        for search in popular_searches:
            if st.sidebar.button(f"🔍 {search}", key=f"search_{search}"):
                st.session_state.pending_query = search
                st.rerun()
        
        st.sidebar.markdown("---")
        
        # Price range selector
        st.sidebar.markdown("**Budget Filter:**")
        min_price = st.sidebar.number_input("Min Price (GHS)", min_value=0, value=0, step=100)
        max_price = st.sidebar.number_input("Max Price (GHS)", min_value=0, value=5000, step=100)
        
        if min_price > 0 or max_price != 5000:
            st.session_state.budget_filter = f"between GHS {min_price} and GHS {max_price}"
        
        st.sidebar.markdown("---")
        
        # Chat controls
        if st.sidebar.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.session_state.current_products = []
            st.rerun()
        
        # Statistics
        if st.session_state.chat_history:
            st.sidebar.markdown("### Chat Statistics")
            user_messages = len([m for m in st.session_state.chat_history if m['role'] == 'user'])
            st.sidebar.metric("Messages Sent", user_messages)
            
            if st.session_state.current_products:
                st.sidebar.metric("Products Found", len(st.session_state.current_products))

def main():
    # Initialize the shopping assistant
    assistant = ShoppingAssistant()
    assistant.initialize_session()
    
    # Header
    st.title("🛍️ AI Shopping Assistant")
    st.markdown("*Your intelligent shopping companion for Jiji.com.gh*")
    
    # Render sidebar
    assistant.render_sidebar()
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Chat container
        chat_container = st.container()
        
        with chat_container:
            # Display welcome message if no chat history
            if not st.session_state.chat_history:
                st.markdown("""
                <div class="chat-message bot-message">
                    <strong>🛍️ Assistant:</strong> 
                    Hello! I'm your AI shopping assistant. I can help you:
                    <br><br>
                    • Find products on Jiji.com.gh within your budget<br>
                    • Track your orders<br>
                    • Answer questions about products<br>
                    • Provide personalized recommendations<br>
                    • Compare products and set price alerts<br>
                    <br>
                    What are you looking for today?
                </div>
                """, unsafe_allow_html=True)
            
            # Display chat history
            assistant.display_chat_history()
        
        # User input
        st.markdown("---")
        user_input = st.text_input(
            "Type your message here...", 
            placeholder="e.g., Find Samsung Galaxy phones under GHS 2000",
            key="user_input"
        )
        
        # Handle button clicks from sidebar
        if 'pending_query' in st.session_state:
            user_input = st.session_state.pending_query
            del st.session_state.pending_query
        
        # Add budget filter to query if set
        if 'budget_filter' in st.session_state and user_input and 'GHS' not in user_input:
            user_input += f" {st.session_state.budget_filter}"
        
        # Process user input
        if user_input:
            with st.spinner("🤔 Thinking..."):
                assistant.process_user_message(user_input)
            st.rerun()
    
    with col2:
        # Additional info panel
        st.markdown("### 💡 Tips")
        st.markdown("""
        **How to search effectively:**
        - Be specific about the product
        - Include your budget range
        - Mention preferred location if any
        
        **Example queries:**
        - "iPhone 13 under GHS 4000"
        - "Gaming laptop between GHS 2000-5000"
        - "Bluetooth headphones in Accra"
        """)
        
        if st.session_state.current_products:
            st.markdown("### 📊 Search Results")
            st.metric("Products Found", len(st.session_state.current_products))
            
            if st.session_state.current_products:
                prices = [float(p.get('price', '0').replace('GH₵', '').replace(',', '')) 
                         for p in st.session_state.current_products 
                         if p.get('price') and p['price'].replace('GH₵', '').replace(',', '').replace(' ', '').isdigit()]
                
                if prices:
                    st.metric("Avg Price", f"GH₵ {sum(prices)/len(prices):,.0f}")
                    st.metric("Price Range", f"GH₵ {min(prices):,.0f} - GH₵ {max(prices):,.0f}")

if __name__ == "__main__":
    main()