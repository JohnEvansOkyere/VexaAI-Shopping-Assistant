import streamlit as st
from typing import Dict, List, Any
from datetime import datetime
import json

class SessionManager:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize all session state variables"""
        default_states = {
            'chat_history': [],
            'current_products': [],
            'user_preferences': {},
            'search_history': [],
            'favorite_products': [],
            'price_alerts': [],
            'user_profile': {
                'preferred_location': 'Accra',
                'budget_range': {'min': 0, 'max': 10000},
                'preferred_categories': []
            }
        }
        
        for key, default_value in default_states.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    def add_to_search_history(self, query: str, results_count: int):
        """Add search to history"""
        search_entry = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'results_count': results_count
        }
        
        # Keep only last 50 searches
        st.session_state.search_history.append(search_entry)
        if len(st.session_state.search_history) > 50:
            st.session_state.search_history = st.session_state.search_history[-50:]
    
    def add_to_favorites(self, product: Dict[str, str]):
        """Add product to favorites"""
        if product not in st.session_state.favorite_products:
            st.session_state.favorite_products.append(product)
            return True
        return False
    
    def remove_from_favorites(self, product_title: str):
        """Remove product from favorites"""
        st.session_state.favorite_products = [
            p for p in st.session_state.favorite_products 
            if p.get('title') != product_title
        ]
    
    def update_user_preferences(self, preferences: Dict[str, Any]):
        """Update user preferences"""
        st.session_state.user_preferences.update(preferences)
    
    def get_recent_searches(self, limit: int = 5) -> List[str]:
        """Get recent search queries"""
        recent = st.session_state.search_history[-limit:] if st.session_state.search_history else []
        return [search['query'] for search in reversed(recent)]
    
    def export_chat_history(self) -> str:
        """Export chat history as JSON"""
        try:
            return json.dumps(st.session_state.chat_history, indent=2, ensure_ascii=False)
        except Exception as e:
            return f"Error exporting chat history: {str(e)}"
    
    def clear_session_data(self, data_type: str = 'all'):
        """Clear specific session data"""
        if data_type == 'all':
            st.session_state.chat_history = []
            st.session_state.current_products = []
            st.session_state.search_history = []
        elif data_type == 'chat':
            st.session_state.chat_history = []
        elif data_type == 'products':
            st.session_state.current_products = []
        elif data_type == 'search_history':
            st.session_state.search_history = []
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        return {
            'total_messages': len(st.session_state.chat_history),
            'user_messages': len([m for m in st.session_state.chat_history if m['role'] == 'user']),
            'products_viewed': len(st.session_state.current_products),
            'searches_performed': len(st.session_state.search_history),
            'favorites_count': len(st.session_state.favorite_products)
        }
    
    def save_user_feedback(self, feedback: Dict[str, Any]):
        """Save user feedback"""
        if 'user_feedback' not in st.session_state:
            st.session_state.user_feedback = []
        
        feedback['timestamp'] = datetime.now().isoformat()
        st.session_state.user_feedback.append(feedback)
    
    def get_user_context(self) -> Dict[str, Any]:
        """Get user context for personalization"""
        return {
            'recent_searches': self.get_recent_searches(),
            'preferences': st.session_state.user_preferences,
            'favorite_categories': self.get_favorite_categories(),
            'average_budget': self.calculate_average_budget()
        }
    
    def get_favorite_categories(self) -> List[str]:
        """Determine user's favorite product categories from history"""
        categories = {}
        
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                content = message['content'].lower()
                if any(word in content for word in ['phone', 'smartphone', 'mobile']):
                    categories['smartphones'] = categories.get('smartphones', 0) + 1
                elif any(word in content for word in ['laptop', 'computer']):
                    categories['laptops'] = categories.get('laptops', 0) + 1
                elif any(word in content for word in ['headphone', 'speaker', 'audio']):
                    categories['audio'] = categories.get('audio', 0) + 1
        
        return sorted(categories.keys(), key=categories.get, reverse=True)
    
    def calculate_average_budget(self) -> Dict[str, float]:
        """Calculate user's average budget from search history"""
        budgets = []
        
        for search in st.session_state.search_history:
            query = search['query'].lower()
            # Extract budget mentions
            import re
            budget_matches = re.findall(r'(\d+(?:,\d{3})*)', query)
            if budget_matches:
                try:
                    budgets.extend([int(b.replace(',', '')) for b in budget_matches])
                except ValueError:
                    continue
        
        if budgets:
            return {
                'average': sum(budgets) / len(budgets),
                'min': min(budgets),
                'max': max(budgets)
            }
        
        return {'average': 2500, 'min': 500, 'max': 5000}  # Defaults