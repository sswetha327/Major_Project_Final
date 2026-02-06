from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random
import re
from urllib.parse import urlparse

def extract_product_name(soup, url):
    """
    Extract product name from webpage using multiple selectors
    """
    # Try multiple selectors for product title
    selectors = [
        "h1#productTitle",
        "h1.product-title",
        "h1.product-name",
        "h1.title",
        "h1",
        ".product-title",
        ".product-name",
        ".title",
        "[data-hook='product-title']",
        "#product-name",
        ".product-name a",
        "span.product-name",
        "div.product-title"
    ]
    
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            name = element.get_text(strip=True)
            if len(name) > 3 and len(name) < 200:  # Reasonable length
                return clean_product_name(name)
    
    # Try to get from title tag as fallback
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.get_text(strip=True)
        # Extract product name from title (usually first part)
        name = title.split('|')[0].split('-')[0].split(':')[0]
        return clean_product_name(name)
    
    # Fallback to URL extraction
    return extract_product_name_from_url(url)

def extract_product_name_from_url(url):
    """
    Extract product name from URL as fallback
    """
    try:
        parsed = urlparse(url)
        path = parsed.path
        
        # Remove common prefixes and extract meaningful part
        name = path.split('/')[-1] if path else ""
        
        # Remove file extensions and query parameters
        name = name.split('.')[0].split('?')[0].split('#')[0]
        
        # Replace URL encoded characters and hyphens with spaces
        name = re.sub(r'[-_]', ' ', name)
        name = re.sub(r'%[0-9A-Fa-f]{2}', '', name)
        
        # Capitalize words
        name = ' '.join(word.capitalize() for word in name.split())
        
        return clean_product_name(name) if name else "Unknown Product"
        
    except Exception:
        return "Unknown Product"

def clean_product_name(name):
    """
    Clean and format product name
    """
    if not name:
        return "Unknown Product"
    
    # Remove extra whitespace
    name = ' '.join(name.split())
    
    # Remove common unwanted suffixes
    unwanted_suffixes = [
        'amazon.com', 'buy now', 'shop now', 'add to cart',
        'free shipping', 'prime', 'best seller', 'deal'
    ]
    
    for suffix in unwanted_suffixes:
        name = name.replace(suffix, '').strip()
    
    # Limit length
    if len(name) > 100:
        name = name[:100].strip()
    
    return name if name else "Unknown Product"

def get_reviews(product_url, max_reviews=20):
    """
    Attempts to scrape reviews and product name from a product URL.
    If scraping fails, returns mock data for demonstration.
    """
    print(f"Attempting to scrape reviews from: {product_url}")
    
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Set a realistic user agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
        options.add_argument(f"user-agent={random.choice(user_agents)}")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        # Execute script to remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        driver.get(product_url)
        time.sleep(random.uniform(3, 6))
        
        # Scroll to load more reviews with random delays
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1, 3))

        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Extract product name
        product_name = extract_product_name(soup, product_url)
        
        # Debug: Print page title to see what we got
        page_title = soup.find('title')
        if page_title:
            print(f"Page title: {page_title.get_text(strip=True)}")
        
        driver.quit()

        reviews = []

        # Enhanced selectors for multiple e-commerce sites
        selectors = [
            # Amazon
            "span[data-hook='review-body']",
            "div[data-hook='review-collapsed'] span",
            "span.review-text-content span",
            "div.review-text span",
            "[data-hook='review-body'] span",
            ".review-text",
            ".a-size-base.review-text",
            ".a-size-base.review-text-content",
            # Flipkart
            "div._1AtVbE div._27M-vq",
            "div.t-ZTKy div",
            "div.ZmyHeo div",
            # Myntra
            "div.user-review div.review-text",
            "div[data-automationid='review-text']",
            # Generic
            ".review-content",
            ".review-body",
            ".customer-review",
            ".product-review",
            "[class*='review']",
            "[id*='review']"
        ]
        
        print(f"Trying {len(selectors)} different selectors...")
        
        for i, selector in enumerate(selectors):
            review_divs = soup.select(selector)
            print(f"Selector {i+1}: '{selector}' found {len(review_divs)} elements")
            
            if review_divs:
                for div in review_divs[:max_reviews]:
                    text = div.get_text(strip=True)
                    if len(text) > 10:  # Filter out very short texts
                        reviews.append({"text": text})
                print(f"Successfully used selector: {selector}")
                break
        
        # If still no reviews, try a more generic approach
        if not reviews:
            print("No specific selectors worked, trying generic approach...")
            # Look for any div or span containing review-like text
            all_text_elements = soup.find_all(['div', 'span'])
            print(f"Found {len(all_text_elements)} total text elements")
            
            for elem in all_text_elements:
                text = elem.get_text(strip=True)
                if len(text) > 50 and ('star' in text.lower() or 'good' in text.lower() or 'bad' in text.lower() or 'product' in text.lower() or 'review' in text.lower()):
                    if len(reviews) < max_reviews:
                        reviews.append({"text": text})
            
            print(f"Generic approach found {len(reviews)} potential reviews")

        if reviews:
            print(f"Successfully scraped {len(reviews)} reviews for: {product_name}")
            return reviews, product_name
        else:
            print("No reviews found, using mock data")
            return get_mock_reviews(max_reviews), product_name
            
    except Exception as e:
        print(f"Scraping failed: {e}")
        print("Using mock data")
        return get_mock_reviews(max_reviews), extract_product_name_from_url(product_url)

def get_mock_reviews(max_reviews=20, product_url="", product_name=""):
    """
    Returns realistic mock review data based on product type.
    """
    # Extract product type from URL or name for more targeted reviews
    product_type = detect_product_type(product_url, product_name)
    
    # Review templates by product type
    review_templates = {
        "electronics": [
            {"text": "Great sound quality for the price! The battery life is impressive - lasts about 8 hours of continuous use. Easy to pair with devices.", "sentiment": "Positive"},
            {"text": "Decent headphones but the noise cancellation could be better. Works well for calls but music quality is just average.", "sentiment": "Neutral"},
            {"text": "Stopped working after 3 months of light use. The build quality feels cheap and customer service was unhelpful with warranty.", "sentiment": "Negative"},
            {"text": "Excellent value! These headphones compete with brands twice the price. Comfortable for long wearing sessions.", "sentiment": "Positive"},
            {"text": "Connection issues are frustrating - keeps dropping Bluetooth connection. Sound quality is good when it stays connected though.", "sentiment": "Negative"},
            {"text": "Good bass response and clear highs. The carrying case is a nice touch. Overall satisfied with the purchase.", "sentiment": "Positive"},
            {"text": "Average quality at best. You get what you pay for. Not suitable for audiophiles but fine for casual listening.", "sentiment": "Neutral"},
            {"text": "Amazing build quality! The metal construction feels premium. Worth every penny for the durability alone.", "sentiment": "Positive"},
            {"text": "Too tight on the head, becomes uncomfortable after 30 minutes. Sound quality doesn't justify the discomfort.", "sentiment": "Negative"},
            {"text": "Works as advertised. No frills but gets the job done. Battery life is the standout feature.", "sentiment": "Neutral"}
        ],
        "clothing": [
            {"text": "Perfect fit! The fabric quality is excellent and the color is exactly as shown in photos. Very satisfied.", "sentiment": "Positive"},
            {"text": "Runs small - order one size up. Material is decent but not as soft as expected.", "sentiment": "Neutral"},
            {"text": "Shrunk after first wash despite following care instructions. Disappointed with the quality for the price.", "sentiment": "Negative"},
            {"text": "Beautiful design and great quality! Gets lots of compliments when I wear it. Highly recommended.", "sentiment": "Positive"},
            {"text": "Comfortable and stylish. The material breathes well so it's good for all-day wear.", "sentiment": "Positive"},
            {"text": "Average quality. Nothing special but works for the price. Expected better material at this price point.", "sentiment": "Neutral"},
            {"text": "Color faded quickly after just a few washes. Fit is good but durability is questionable.", "sentiment": "Negative"},
            {"text": "Exactly what I was looking for! The attention to detail is impressive. Will buy from this brand again.", "sentiment": "Positive"},
            {"text": "Sizing is inconsistent with other brands. Quality is okay but the fit issues are frustrating.", "sentiment": "Negative"},
            {"text": "Good basic item. Does what it's supposed to do. Not fashion-forward but practical.", "sentiment": "Neutral"}
        ],
        "furniture": [
            {"text": "Excellent quality furniture! Sturdy construction and easy to assemble. Looks more expensive than it was.", "sentiment": "Positive"},
            {"text": "Assembly took 4 hours and some parts didn't align properly. Once assembled, it's decent but the process was frustrating.", "sentiment": "Neutral"},
            {"text": "Wobbly and unstable. Doesn't feel safe for daily use. Particle board construction is disappointing.", "sentiment": "Negative"},
            {"text": "Perfect size for my space! The finish is beautiful and it was much easier to assemble than expected.", "sentiment": "Positive"},
            {"text": "Good value for money. Not premium quality but serves its purpose well. Instructions could be clearer.", "sentiment": "Neutral"},
            {"text": "Scratches easily and shows wear quickly. Looks good from a distance but up close quality is lacking.", "sentiment": "Negative"},
            {"text": "Solid construction and stylish design. Exceeded my expectations for flat-pack furniture.", "sentiment": "Positive"},
            {"text": "Average quality. You get what you pay for. Suitable for temporary use but not long-term investment.", "sentiment": "Neutral"},
            {"text": "Missing hardware made assembly impossible. Customer service was slow to send replacement parts.", "sentiment": "Negative"},
            {"text": "Beautiful piece that transformed my room! Sturdy and well-made. Worth every penny.", "sentiment": "Positive"}
        ],
        "general": [
            {"text": "This product is absolutely amazing! The quality exceeded my expectations and the price is very reasonable.", "sentiment": "Positive"},
            {"text": "I'm quite disappointed with this purchase. The product stopped working after just a week of use.", "sentiment": "Negative"},
            {"text": "It's an okay product. Does what it's supposed to do but nothing extraordinary.", "sentiment": "Neutral"},
            {"text": "Excellent product! Fast shipping and great customer service. The quality is top-notch.", "sentiment": "Positive"},
            {"text": "Not worth the money. Poor quality materials and the design is flawed.", "sentiment": "Negative"},
            {"text": "Good value for money. The product works well and meets my needs. No complaints so far.", "sentiment": "Positive"},
            {"text": "Average quality. It works but I've seen better products in this price range.", "sentiment": "Neutral"},
            {"text": "I love this product! It has made my life so much easier. Highly recommended!", "sentiment": "Positive"},
            {"text": "Could be better. The design needs improvement and the materials feel cheap.", "sentiment": "Negative"},
            {"text": "Pretty good overall. Some minor issues but nothing deal-breaking.", "sentiment": "Neutral"}
        ]
    }
    
    # Get appropriate reviews for product type
    templates = review_templates.get(product_type, review_templates["general"])
    
    # Add variety by randomizing and adding product-specific elements
    import random
    selected_reviews = []
    
    for i in range(min(max_reviews, len(templates))):
        template = templates[i]
        # Add product-specific customization
        customized_text = customize_review(template["text"], product_name, product_type)
        selected_reviews.append({
            "text": customized_text,
            "sentiment": template["sentiment"]
        })
    
    # Shuffle for variety
    random.shuffle(selected_reviews)
    return selected_reviews

def detect_product_type(product_url, product_name):
    """
    Detect product type from URL or name
    """
    url_lower = product_url.lower()
    name_lower = product_name.lower()
    
    # Electronics keywords
    electronics_keywords = [
        'headphone', 'phone', 'laptop', 'tablet', 'camera', 'speaker', 'bluetooth',
        'wireless', 'charger', 'battery', 'electronic', 'gadget', 'tech'
    ]
    
    # Clothing keywords
    clothing_keywords = [
        'shirt', 'pants', 'dress', 'shoes', 'jacket', 'cloth', 'wear', 'fashion',
        'clothing', 'apparel', 'outfit', 'wardrobe'
    ]
    
    # Furniture keywords
    furniture_keywords = [
        'table', 'chair', 'sofa', 'bed', 'shelf', 'cabinet', 'furniture',
        'wardrobe', 'desk', 'storage', 'almira', 'sofa'
    ]
    
    # Check keywords
    for keyword in electronics_keywords:
        if keyword in url_lower or keyword in name_lower:
            return "electronics"
    
    for keyword in clothing_keywords:
        if keyword in url_lower or keyword in name_lower:
            return "clothing"
    
    for keyword in furniture_keywords:
        if keyword in url_lower or keyword in name_lower:
            return "furniture"
    
    return "general"

def customize_review(text, product_name, product_type):
    """
    Customize review text with product-specific details
    """
    if not product_name or product_name == "Unknown Product":
        return text
    
    # Add product name to some reviews
    import random
    if random.random() < 0.3:  # 30% chance to mention product
        text = text.replace("This product", f"This {product_name}")
    
    # Add type-specific details
    if product_type == "electronics":
        if random.random() < 0.2:
            text += " The tech features are impressive."
    elif product_type == "clothing":
        if random.random() < 0.2:
            text += " The fit and finish are excellent."
    elif product_type == "furniture":
        if random.random() < 0.2:
            text += " Assembly was straightforward."
    
    return text


# TEST BLOCK — DO NOT REMOVE
if __name__ == "__main__":
    url = "https://www.amazon.in/product-reviews/B0CHX7HK9Y"
    data = get_reviews(url)
    print(data)
