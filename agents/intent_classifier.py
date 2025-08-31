import re
from typing import Dict, List, Any

class IntentClassifier:
    def __init__(self):
        self.intent_patterns = {
            'search_product': [
                r'\b(find|search|look for|want|need|buy|purchase|shopping for)\b',
                r'\b(phone|laptop|computer|headphone|tablet|camera|watch)\b',
                r'\b(samsung|iphone|apple|hp|dell|sony|lg|tecno|infinix)\b',
                r'\b(under|below|within|budget|price|cost|ghs|₵)\b'
            ],
            'track_order': [
                r'\b(track|order|delivery|shipment|status)\b',
                r'\b(order number|tracking|delivered|shipped)\b'
            ],
            'faq_inquiry': [
                r'\b(help|how|what|why|when|where|support|question)\b',
                r'\b(return|refund|warranty|payment|shipping|policy)\b'
            ],
            'get_recommendations': [
                r'\b(recommend|suggest|advice|best|top|popular|similar)\b',
                r'\b(what should|which one|alternatives)\b'
            ],
            'compare_products': [
                r'\b(compare|vs|versus|difference|better|between)\b',
                r'\b(which is better|what\'s the difference)\b'
            ],
            'price_alert': [
                r'\b(alert|notify|watch|monitor|price drop|when price)\b',
                r'\b(let me know|tell me when|notification)\b'
            ]
        }
        
        self.product_keywords = [
            'phone', 'smartphone', 'iphone', 'samsung', 'galaxy', 'android',
            'laptop', 'computer', 'macbook', 'hp', 'dell', 'lenovo',
            'tablet', 'ipad', 'headphone', 'airpods', 'speaker',
            'camera', 'watch', 'smartwatch', 'tv', 'monitor',
            'gaming', 'console', 'playstation', 'xbox',
            'car', 'vehicle', 'toyota', 'honda', 'mercedes'
        ]
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract relevant entities from user input"""
        entities = {
            'product_type': [],
            'brand': [],
            'budget': {},
            'location': [],
            'specifications': []
        }
        
        text_lower = text.lower()
        
        # Extract product types
        for keyword in self.product_keywords:
            if keyword in text_lower:
                entities['product_type'].append(keyword)
        
        # Extract brands
        brands = ['samsung', 'apple', 'iphone', 'hp', 'dell', 'lenovo', 'sony', 'lg', 'tecno', 'infinix']
        for brand in brands:
            if brand in text_lower:
                entities['brand'].append(brand)
        
        # Extract budget information
        budget_patterns = [
            r'(?:under|below|less than|maximum|max)\s*(?:ghs?\s*)?(\d+(?:,\d{3})*)',
            r'(?:ghs?\s*)?(\d+(?:,\d{3})*)\s*(?:to|and|-|or)\s*(?:ghs?\s*)?(\d+(?:,\d{3})*)',
            r'budget\s*(?:of|is)?\s*(?:ghs?\s*)?(\d+(?:,\d{3})*)',
            r'between\s*(?:ghs?\s*)?(\d+(?:,\d{3})*)\s*(?:and|to|-)\s*(?:ghs?\s*)?(\d+(?:,\d{3})*)'
        ]
        
        for pattern in budget_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                groups = match.groups()
                if len(groups) == 1:  # Single amount (under/below)
                    entities['budget']['max'] = int(groups[0].replace(',', ''))
                elif len(groups) == 2:  # Range
                    entities['budget']['min'] = int(groups[0].replace(',', ''))
                    entities['budget']['max'] = int(groups[1].replace(',', ''))
        
        # Extract specifications
        spec_patterns = [
            r'(\d+)\s*gb',
            r'(\d+)\s*tb',
            r'(\d+)\s*inch',
            r'(\d+)\s*mp',
            r'(\d+)\s*core'
        ]
        
        for pattern in spec_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                entities['specifications'].append(f"{match} {pattern.split('\\')[1].split(')')[0]}")
        
        # Extract locations
        ghana_cities = ['accra', 'kumasi', 'tamale', 'cape coast', 'tema', 'sekondi', 'koforidua']
        for city in ghana_cities:
            if city in text_lower:
                entities['location'].append(city.title())
        
        return entities
    
    def classify_intent(self, text: str) -> Dict[str, Any]:
        """Classify user intent based on input text"""
        text_lower = text.lower()
        intent_scores = {}
        
        # Calculate scores for each intent
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches
            intent_scores[intent] = score
        
        # Determine primary intent
        if not any(intent_scores.values()):
            primary_intent = 'general_chat'
        else:
            primary_intent = max(intent_scores, key=intent_scores.get)
        
        # Extract entities
        entities = self.extract_entities(text)
        
        return {
            'intent': primary_intent,
            'confidence': max(intent_scores.values()) if intent_scores.values() else 0,
            'entities': entities,
            'all_scores': intent_scores
        }
    
    def get_intent_explanation(self, intent: str) -> str:
        """Get explanation for detected intent"""
        explanations = {
            'search_product': "I'll help you search for products on Jiji.com.gh",
            'track_order': "I'll help you track your order status",
            'faq_inquiry': "I'll answer your question or help with support",
            'get_recommendations': "I'll provide personalized product recommendations",
            'compare_products': "I'll help you compare different products",
            'price_alert': "I'll set up a price alert for you",
            'general_chat': "I'm here to help with your shopping needs"
        }
        return explanations.get(intent, "I'll help you with that")