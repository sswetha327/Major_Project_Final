from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def debug_page(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(url)
    time.sleep(5)
    
    # Scroll to load more reviews
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Save HTML to file for inspection
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(str(soup.prettify()))
    
    print("Page source saved to page_source.html")
    
    # Look for any review-related elements
    review_elements = soup.find_all(attrs={"data-hook": lambda x: x and "review" in x})
    print(f"\nFound {len(review_elements)} elements with 'review' in data-hook:")
    for elem in review_elements[:5]:
        print(f"  - {elem.name}[data-hook={elem.get('data-hook')}]")
    
    driver.quit()

if __name__ == "__main__":
    url = "https://www.amazon.in/product-reviews/B0CHX7HK9Y"
    debug_page(url)
