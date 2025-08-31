import requests
from bs4 import BeautifulSoup
import re
import time
from typing import List, Dict, Tuple, Any
import streamlit as st

class ProductAgent:
    def __init__(self):
        self.base_url = "https://jiji.com.gh"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def clean_price(self, price_text: str) -> str:
        """Clean and standardize price text"""
        if not price_text:
            return "Price not available"
        
        # Remove extra whitespace and normalize
        price = re.sub(r'\s+', ' ', price_text.strip())
        
        # Ensure proper GH₵ format
        if 'gh₵' in price.lower() or '₵' in price:
            return price
        elif any(char.isdigit() for char in price):
            # Add GH₵ if missing
            return f"GH₵ {price}"
        
        return price
    
    def parse_product_card(self, product_element) -> Dict[str, str]:
        """Parse individual product card from Jiji"""
        try:
            product = {}
            
            # Extract title
            title_elem = product_element.find('a', class_='b-list-advert__item__title')
            if not title_elem:
                title_elem = product_element.find('h3') or product_element.find('a')
            
            product['title'] = title_elem.get_text(strip=True) if title_elem else "Product Title"
            
            # Extract link
            link_elem = product_element.find('a', href=True)
            if link_elem:
                href = link_elem['href']
                product['link'] = href if href.startswith('http') else f"{self.base_url}{href}"
            else:
                product['link'] = "#"
            
            # Extract price
            price_elem = (product_element.find('div', class_='b-list-advert__item__price') or
                         product_element.find('span', class_='qa-advert-price') or
                         product_element.find('div', string=re.compile(r'GH₵|₵')))
            
            if price_elem:
                product['price'] = self.clean_price(price_elem.get_text(strip=True))
            else:
                product['price'] = "Price on request"
            
            # Extract location
            location_elem = (product_element.find('div', class_='b-list-advert__item__location') or
                           product_element.find('span', class_='qa-advert-location'))
            
            product['location'] = location_elem.get_text(strip=True) if location_elem else "Ghana"
            
            return product
            
        except Exception as e:
            st.error(f"Error parsing product: {str(e)}")
            return {
                'title': "Product parsing error",
                'price': "N/A",
                'link': "#",
                'location': "Ghana"
            }
    
    def scrape_jiji_products(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """Scrape products from Jiji.com.gh"""
        try:
            # Format search query for URL
            search_query = query.replace(' ', '-').lower()
            search_url = f"{self.base_url}/search?query={requests.utils.quote(query)}"
            
            # Alternative search URLs to try
            search_urls = [
                f"{self.base_url}/search?query={requests.utils.quote(query)}",
                f"{self.base_url}/ghana/cars/all-cars?query={requests.utils.quote(query)}",
                f"{self.base_url}/ghana/mobile-phones?query={requests.utils.quote(query)}"
            ]
            
            products = []
            
            for url in search_urls:
                try:
                    response = self.session.get(url, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Find product containers (multiple selectors for robustness)
                        product_selectors = [
                            'div.b-list-advert__item',
                            'div[data-testid="advert-list-item"]',
                            'div.qa-advert-list-item',
                            'article',
                            'div.advert-card'
                        ]
                        
                        product_elements = []
                        for selector in product_selectors:
                            elements = soup.select(selector)
                            if elements:
                                product_elements = elements
                                break
                        
                        # Parse products
                        for element in product_elements[:max_results]:
                            product = self.parse_product_card(element)
                            if product['title'] != "Product parsing error":
                                products.append(product)
                        
                        if products:
                            break  # Found products, no need to try other URLs
                            
                except Exception as e:
                    continue  # Try next URL
            
            return products[:max_results]
            
        except Exception as e:
            st.error(f"Error scraping Jiji: {str(e)}")
            return self.get_sample_products(query)  # Fallback to sample data
    
    def get_sample_products(self, query: str) -> List[Dict[str, str]]:
        """Fallback sample products when scraping fails"""
        sample_products = [
            {
                'title': f"Samsung Galaxy S20 Ultra 128GB - {query}",
                'price': "GH₵ 4,200",
                'link': "https://jiji.com.gh/sample-product-1",
                'location': "Accra, Greater Accra"
            },
            {
                'title': f"Samsung Galaxy S20 Ultra 256GB - {query}",
                'price': "GH₵ 4,800",
                'link': "https://jiji.com.gh/sample-product-2",
                'location': "Kumasi, Ashanti"
            },
            {
                'title': f"Samsung Galaxy S20 Ultra (Used) - {query}",
                'price': "GH₵ 3,500",
                'link': "https://jiji.com.gh/sample-product-3",
                'location': "Tema, Greater Accra"
            }
        ]
        return sample_products
    
    def filter_by_budget(self, products: List[Dict[str, str]], budget: Dict[str, int]) -> List[Dict[str, str]]:
        """Filter products by budget constraints"""
        if not budget:
            return products
        
        filtered_products = []
        
        for product in products:
            try:
                # Extract numeric price
                price_text = product.get('price', '0')
                price_match = re.search(r'[\d,]+', price_text.replace('GH₵', '').replace('₵', ''))
                
                if price_match:
                    price = int(price_match.group().replace(',', ''))
                    
                    # Check budget constraints
                    within_budget = True
                    if 'min' in budget and price < budget['min']:
                        within_budget = False
                    if 'max' in budget and price > budget['max']:
                        within_budget = False
                    
                    if within_budget:
                        filtered_products.append(product)
                        
            except (ValueError, AttributeError):
                # Include products with unparseable prices
                filtered_products.append(product)
        
        return filtered_products
    
    def search_products(self, query: str, entities: Dict[str, Any]) -> Tuple[str, List[Dict[str, str]]]:
        """Main product search function"""
        try:
            # Build search query from entities
            search_terms = []
            
            if entities.get('product_type'):
                search_terms.extend(entities['product_type'])
            if entities.get('brand'):
                search_terms.extend(entities['brand'])
            if entities.get('specifications'):
                search_terms.extend(entities['specifications'])
            
            # Use original query if no specific terms found
            if not search_terms:
                search_query = query
            else:
                search_query = ' '.join(search_terms)
            
            # Scrape products
            with st.spinner("🔍 Searching Jiji.com.gh..."):
                products = self.scrape_jiji_products(search_query)
            
            # Filter by budget if specified
            if entities.get('budget'):
                products = self.filter_by_budget(products, entities['budget'])
            
            # Store products in session state
            st.session_state.current_products = products
            
            # Generate response
            if not products:
                response = f"""
                Sorry, I couldn't find any products matching "{query}" on Jiji.com.gh. 
                
                **Suggestions:**
                • Try different keywords (e.g., "Galaxy" instead of "Samsung Galaxy")
                • Check your budget range
                • Try a broader search term
                • Visit [Jiji.com.gh]({self.base_url}) directly
                """
            else:
                budget_text = ""
                if entities.get('budget'):
                    if 'min' in entities['budget'] and 'max' in entities['budget']:
                        budget_text = f" within GHS {entities['budget']['min']:,} - GHS {entities['budget']['max']:,}"
                    elif 'max' in entities['budget']:
                        budget_text = f" under GHS {entities['budget']['max']:,}"
                
                response = f"""
                Great! I found **{len(products)} products** matching "{query}"{budget_text} on Jiji.com.gh:
                
                Here are the best matches for you:
                """
            
            return response, products
            
        except Exception as e:
            error_response = f"""
            Sorry, I encountered an error while searching for products: {str(e)}
            
            Please try:
            • Refreshing the page and trying again
            • Using simpler search terms
            • Visiting [Jiji.com.gh]({self.base_url}) directly
            """
            return error_response, []
    
    def compare_products(self, query: str, entities: Dict[str, Any]) -> str:
        """Compare products functionality"""
        return """
        **Product Comparison** (Coming Soon!)
        
        I'll soon be able to help you compare:
        • Specifications side-by-side
        • Price differences
        • Pros and cons
        • User ratings and reviews
        
        For now, try searching for specific products and I'll show you multiple options to compare manually.
        """
    
    def set_price_alert(self, query: str, entities: Dict[str, Any]) -> str:
        """Set price alert functionality"""
        return """
        **Price Alerts** (Coming Soon!)
        
        Soon you'll be able to:
        • Set alerts for specific products
        • Get notified when prices drop
        • Track price history
        • Set budget thresholds
        
        For now, bookmark products you're interested in and check back regularly!
        """