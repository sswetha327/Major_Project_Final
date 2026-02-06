from scraper.scraper import get_reviews
from sentiment.sentiment import analyze_sentiment

# Amazon product review URL
url = "https://www.amazon.in/product-reviews/B0CHX7HK9Y"

# Step 1: get reviews
reviews = get_reviews(url)

# Step 2: analyze sentiment for each review
for r in reviews:
    sentiment = analyze_sentiment(r["text"])
    r["sentiment"] = sentiment

# Step 3: print final result
print(reviews)
