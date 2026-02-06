#!/usr/bin/env python3
"""
Test script to verify MongoDB Atlas connection
"""
import os
from database.connection import db_connection
from database.models import product_model

def test_connection():
    print("Testing MongoDB Atlas connection...")
    
    # Test basic connection
    if db_connection.connect():
        print("✅ Successfully connected to MongoDB Atlas")
        
        # Test database operations
        try:
            # Test creating a sample product
            sample_data = {
                "summary": {"Positive": 1, "Negative": 0, "Neutral": 0},
                "reviews": [{"text": "Great product!", "sentiment": "Positive"}]
            }
            
            product_id = product_model.create_product(
                "Test Product", 
                "https://example.com/test", 
                sample_data
            )
            print(f"✅ Successfully created test product with ID: {product_id}")
            
            # Test retrieving the product
            retrieved_product = product_model.get_product_by_id(product_id)
            if retrieved_product:
                print("✅ Successfully retrieved test product")
            else:
                print("❌ Failed to retrieve test product")
            
            # Test deleting the test product
            if product_model.delete_product(product_id):
                print("✅ Successfully cleaned up test product")
            else:
                print("❌ Failed to clean up test product")
                
        except Exception as e:
            print(f"❌ Database operation failed: {e}")
        
        # Close connection
        db_connection.disconnect()
        print("✅ Connection closed successfully")
        
    else:
        print("❌ Failed to connect to MongoDB Atlas")
        print("Please check your connection string and credentials in .env file")

if __name__ == "__main__":
    test_connection()
