from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random

def get_reviews(product_url, max_reviews=20):
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
    driver.quit()

    reviews = []

    # Try multiple selectors for Amazon reviews
    selectors = [
        "span[data-hook='review-body']",
        "div[data-hook='review-collapsed'] span",
        "span.review-text-content span",
        "div.review-text span",
        "[data-hook='review-body'] span",
        ".review-text",
        ".a-size-base.review-text",
        ".a-size-base.review-text-content"
    ]
    
    for selector in selectors:
        review_divs = soup.select(selector)
        if review_divs:
            for div in review_divs[:max_reviews]:
                text = div.get_text(strip=True)
                if len(text) > 10:  # Filter out very short texts
                    reviews.append({"text": text})
            break
    
    # If still no reviews, try a more generic approach
    if not reviews:
        # Look for any div or span containing review-like text
        all_text_elements = soup.find_all(['div', 'span'])
        for elem in all_text_elements:
            text = elem.get_text(strip=True)
            if len(text) > 50 and ('star' in text.lower() or 'good' in text.lower() or 'bad' in text.lower() or 'product' in text.lower()):
                if len(reviews) < max_reviews:
                    reviews.append({"text": text})

    return reviews

# Test the scraper
if __name__ == "__main__":
    url = "https://www.amazon.in/product-reviews/B0CHX7HK9Y"
    data = get_reviews(url)
    print(f"Found {len(data)} reviews:")
    for i, review in enumerate(data[:5], 1):
        print(f"\nReview {i}:")
        print(review["text"][:200] + "..." if len(review["text"]) > 200 else review["text"])
