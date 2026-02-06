#!/usr/bin/env python3
"""
Check Stored URLs in Database
Shows all products and URLs that have been analyzed
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.connection import db_connection

def check_stored_urls():
    print("🔍 Checking Stored URLs in Database")
    print("=" * 50)
    
    # Connect to database if not already connected
    if not db_connection.is_connected():
        print("🔌 Connecting to database...")
        if not db_connection.connect():
            print("❌ Failed to connect to database")
            print("Please ensure MongoDB is configured properly")
            return
    
    try:
        from database.models import product_model
        
        # Get all products
        products = product_model.get_all_products()
        
        if not products:
            print("📭 No products stored yet")
            print("Analyze some products first to see them here")
            return
        
        print(f"📊 Found {len(products)} stored products:")
        print("-" * 50)
        
        for i, product in enumerate(products, 1):
            print(f"\n{i}. **Product**: {product['product_name']}")
            print(f"   🔗 **URL**: {product['product_url']}")
            print(f"   📅 **Created**: {product['created_at']}")
            print(f"   📈 **Reviews**: {product['total_reviews']} total")
            print(f"   🎯 **Sentiment Summary**: {product['sentiment_summary']}")
            print(f"   🆔 **Database ID**: {product['_id']}")
            print("-" * 30)
        
        # Summary statistics
        total_reviews = sum(p['total_reviews'] for p in products)
        print(f"\n📈 **Summary Statistics**:")
        print(f"   Total Products: {len(products)}")
        print(f"   Total Reviews Analyzed: {total_reviews}")
        
        # Show sentiment breakdown across all products
        all_positive = sum(p['sentiment_summary'].get('Positive', 0) for p in products)
        all_negative = sum(p['sentiment_summary'].get('Negative', 0) for p in products)
        all_neutral = sum(p['sentiment_summary'].get('Neutral', 0) for p in products)
        
        print(f"   Overall Sentiment:")
        print(f"     😊 Positive: {all_positive}")
        print(f"     😠 Negative: {all_negative}")
        print(f"     😐 Neutral: {all_neutral}")
        
    except Exception as e:
        print(f"❌ Error retrieving data: {e}")

def check_specific_url(url):
    print(f"\n🔍 Checking Specific URL: {url}")
    print("-" * 50)
    
    try:
        from database.models import product_model
        
        product = product_model.get_product_by_url(url)
        
        if product:
            print("✅ **URL Found in Database**")
            print(f"   Product Name: {product['product_name']}")
            print(f"   Created: {product['created_at']}")
            print(f"   Total Reviews: {product['total_reviews']}")
            print(f"   Sentiment Summary: {product['sentiment_summary']}")
            print(f"   Database ID: {product['_id']}")
            
            # Show first few reviews as sample
            print(f"\n   Sample Reviews (first 3):")
            for i, review in enumerate(product['reviews'][:3], 1):
                print(f"     {i}. [{review['sentiment']}] {review['text'][:60]}...")
                
        else:
            print("❌ **URL Not Found in Database**")
            print("   This URL hasn't been analyzed yet")
            
    except Exception as e:
        print(f"❌ Error checking URL: {e}")

if __name__ == "__main__":
    # Show all stored URLs
    check_stored_urls()
    
    # Example: Check specific URLs that were analyzed
    print("\n" + "="*50)
    print("🔍 Checking Specific URLs:")
    
    urls_to_check = [
        "https://example.com/test-product",
        "https://www.amazon.com/test-product",
        "https://www.myntra.com/mailers/watches/joker-&-witch/joker-&-witch-women-gold-&-rose-toned-watch-gift-set-jwlt543/23802300/buy"
    ]
    
    for url in urls_to_check:
        check_specific_url(url)
    
    # You can also check any URL manually:
    # check_specific_url("your-url-here")
