from datetime import datetime
from typing import List, Dict, Any
from .connection import db_connection

class ProductModel:
    def __init__(self):
        self.collection = db_connection.get_collection('products')
    
    def create_product(self, product_name: str, product_url: str, reviews_data: List[Dict[str, Any]]) -> str:
        product_document = {
            'product_name': product_name,
            'product_url': product_url,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'sentiment_summary': reviews_data['summary'],
            'total_reviews': len(reviews_data['reviews']),
            'reviews': reviews_data['reviews']
        }
        
        result = self.collection.insert_one(product_document)
        return str(result.inserted_id)
    
    def get_product_by_url(self, product_url: str) -> Dict[str, Any]:
        return self.collection.find_one({'product_url': product_url})
    
    def get_product_by_id(self, product_id: str) -> Dict[str, Any]:
        from bson.objectid import ObjectId
        return self.collection.find_one({'_id': ObjectId(product_id)})
    
    def get_all_products(self) -> List[Dict[str, Any]]:
        return list(self.collection.find({}, {'product_name': 1, 'product_url': 1, 'created_at': 1, 'sentiment_summary': 1, 'total_reviews': 1}))
    
    def update_product_sentiment(self, product_id: str, reviews_data: Dict[str, Any]) -> bool:
        from bson.objectid import ObjectId
        
        update_data = {
            'sentiment_summary': reviews_data['summary'],
            'total_reviews': len(reviews_data['reviews']),
            'reviews': reviews_data['reviews'],
            'updated_at': datetime.utcnow()
        }
        
        result = self.collection.update_one(
            {'_id': ObjectId(product_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def delete_product(self, product_id: str) -> bool:
        from bson.objectid import ObjectId
        result = self.collection.delete_one({'_id': ObjectId(product_id)})
        return result.deleted_count > 0

class ReviewModel:
    def __init__(self):
        self.collection = db_connection.get_collection('reviews')
    
    def get_reviews_by_sentiment(self, sentiment: str, limit: int = 100) -> List[Dict[str, Any]]:
        return list(self.collection.find({'sentiment': sentiment}).limit(limit))
    
    def search_reviews_by_text(self, search_term: str) -> List[Dict[str, Any]]:
        return list(self.collection.find({'text': {'$regex': search_term, '$options': 'i'}}))

product_model = ProductModel()
review_model = ReviewModel()
