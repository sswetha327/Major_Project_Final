from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from scraper.scraper import get_reviews
from sentiment.sentiment import analyze_sentiment
from database.connection import db_connection
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3004", "http://localhost:3005"])

# Initialize database connection
db_connected = db_connection.connect()

# Import models only if database is connected
product_model = None
review_model = None
if db_connected:
    from database.models import product_model, review_model


# Home route (just to check server is running)
@app.route("/")
def home():
    return "Product Sentiment Analyzer Backend Running"


# Database status endpoint
@app.route("/database-status", methods=["GET"])
def database_status():
    try:
        status = {
            "database_connected": db_connected,
            "database_name": os.getenv('DB_NAME', 'product_sentiment_db'),
            "connection_configured": bool(os.getenv('MONGODB_CONNECTION_STRING') and 'your_username' not in os.getenv('MONGODB_CONNECTION_STRING', '')),
            "features_available": {
                "store_products": db_connected and product_model is not None,
                "retrieve_products": db_connected and product_model is not None,
                "search_reviews": db_connected and review_model is not None
            }
        }
        
        if db_connected and product_model:
            try:
                products_count = len(product_model.get_all_products())
                status["products_stored"] = products_count
            except:
                status["products_stored"] = "Error retrieving count"
        
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": f"Status check failed: {str(e)}"}), 500


# Main API route
@app.route("/analyze-product", methods=["POST"])
def analyze_product():
    data = request.get_json()

    # Validate input
    if not data or "url" not in data:
        return jsonify({"error": "Product review URL is required"}), 400

    product_url = data["url"]
    product_name = data.get("product_name", "Unknown Product")

    # Check if product already exists (only if database is connected)
    if db_connected and product_model:
        existing_product = product_model.get_product_by_url(product_url)
        if existing_product:
            return jsonify({
                "message": "Product already analyzed",
                "product_id": str(existing_product["_id"]),
                "summary": existing_product["sentiment_summary"],
                "reviews": existing_product["reviews"]
            })

    # Step 1: Scrape reviews and get product name
    reviews_data = get_reviews(product_url)
    
    # Handle both old format (just reviews) and new format (reviews, product_name)
    if isinstance(reviews_data, tuple) and len(reviews_data) == 2:
        reviews, extracted_product_name = reviews_data
    else:
        # Backward compatibility for old scraper format
        reviews = reviews_data
        extracted_product_name = product_name
    
    # Use extracted product name if available, otherwise use provided name
    final_product_name = extracted_product_name if extracted_product_name != "Unknown Product" else product_name

    # Step 2: Sentiment analysis
    summary = {
        "Positive": 0,
        "Negative": 0,
        "Neutral": 0
    }

    final_reviews = []

    for r in reviews:
        sentiment = analyze_sentiment(r["text"])
        summary[sentiment] += 1
        final_reviews.append({
            "text": r["text"],
            "sentiment": sentiment
        })

    reviews_data = {
        "summary": summary,
        "reviews": final_reviews
    }

    # Step 3: Store in MongoDB (only if connected)
    if db_connected and product_model:
        try:
            product_id = product_model.create_product(final_product_name, product_url, reviews_data)
            
            # Step 4: Return JSON response
            return jsonify({
                "message": "Product analyzed and stored successfully",
                "product_id": product_id,
                "product_name": final_product_name,
                "summary": summary,
                "reviews": final_reviews
            })
        except Exception as e:
            return jsonify({"error": f"Failed to store data: {str(e)}"}), 500
    else:
        # Return response without storing in database
        return jsonify({
            "message": "Product analyzed successfully (not stored - database not configured)",
            "product_name": final_product_name,
            "summary": summary,
            "reviews": final_reviews
        })


# Get all products
@app.route("/products", methods=["GET"])
def get_all_products():
    if not db_connected or not product_model:
        return jsonify({"error": "Database not connected. Configure MongoDB to use this endpoint."}), 503
    
    try:
        products = product_model.get_all_products()
        # Convert ObjectId to string for JSON serialization
        for product in products:
            product['_id'] = str(product['_id'])
            # Convert datetime to string for JSON
            if 'created_at' in product:
                product['created_at'] = str(product['created_at'])
            if 'updated_at' in product:
                product['updated_at'] = str(product['updated_at'])
        return jsonify({"products": products, "total": len(products)})
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve products: {str(e)}"}), 500


# Get specific product by ID
@app.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
    if not db_connected or not product_model:
        return jsonify({"error": "Database not connected. Configure MongoDB to use this endpoint."}), 503
    
    try:
        product = product_model.get_product_by_id(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        product['_id'] = str(product['_id'])
        return jsonify({"product": product})
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve product: {str(e)}"}), 500


# Get reviews by sentiment
@app.route("/reviews/sentiment/<sentiment>", methods=["GET"])
def get_reviews_by_sentiment(sentiment):
    if not db_connected or not review_model:
        return jsonify({"error": "Database not connected. Configure MongoDB to use this endpoint."}), 503
    
    try:
        if sentiment not in ["Positive", "Negative", "Neutral"]:
            return jsonify({"error": "Invalid sentiment. Must be Positive, Negative, or Neutral"}), 400
        
        limit = request.args.get('limit', 100, type=int)
        reviews = review_model.get_reviews_by_sentiment(sentiment, limit)
        
        # Convert ObjectId to string for JSON serialization
        for review in reviews:
            review['_id'] = str(review['_id'])
        
        return jsonify({"reviews": reviews, "sentiment": sentiment, "count": len(reviews)})
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve reviews: {str(e)}"}), 500


# Search reviews by text
@app.route("/reviews/search", methods=["GET"])
def search_reviews():
    if not db_connected or not review_model:
        return jsonify({"error": "Database not connected. Configure MongoDB to use this endpoint."}), 503
    
    try:
        search_term = request.args.get('q')
        if not search_term:
            return jsonify({"error": "Search query parameter 'q' is required"}), 400
        
        reviews = review_model.search_reviews_by_text(search_term)
        
        # Convert ObjectId to string for JSON serialization
        for review in reviews:
            review['_id'] = str(review['_id'])
        
        return jsonify({"reviews": reviews, "search_term": search_term, "count": len(reviews)})
    except Exception as e:
        return jsonify({"error": f"Failed to search reviews: {str(e)}"}), 500


# Delete product
@app.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    if not db_connected or not product_model:
        return jsonify({"error": "Database not connected. Configure MongoDB to use this endpoint."}), 503
    
    try:
        success = product_model.delete_product(product_id)
        if not success:
            return jsonify({"error": "Product not found or deletion failed"}), 404
        
        return jsonify({"message": "Product deleted successfully"})
    except Exception as e:
        return jsonify({"error": f"Failed to delete product: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
