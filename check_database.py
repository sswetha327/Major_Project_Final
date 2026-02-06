#!/usr/bin/env python3
"""
Database Health Check Script
Tests MongoDB connection and basic operations
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.connection import db_connection

def check_database_health():
    print("🔍 Database Health Check")
    print("=" * 50)
    
    # Test 1: Connection Status
    print("\n1. Testing Database Connection...")
    if db_connection.is_connected():
        print("✅ Database is connected")
    else:
        print("❌ Database is NOT connected")
        print("\n📋 To fix this:")
        print("   1. Set up MongoDB Atlas following DATABASE_SETUP.md")
        print("   2. Update .env file with your connection string")
        print("   3. Replace 'your_username' and 'your_password' with actual credentials")
        return False
    
    # Test 2: Basic Operations (only if connected)
    print("\n2. Testing Basic Database Operations...")
    
    try:
        # Import models only after confirming connection
        from database.models import ProductModel, ReviewModel
        product_model = ProductModel()
        review_model = ReviewModel()
        
        # Create test data
        test_data = {
            "summary": {"Positive": 2, "Negative": 1, "Neutral": 1},
            "reviews": [
                {"text": "Great product!", "sentiment": "Positive"},
                {"text": "Average quality", "sentiment": "Neutral"},
                {"text": "Poor experience", "sentiment": "Negative"},
                {"text": "Love it!", "sentiment": "Positive"}
            ]
        }
        
        # Test Create
        product_id = product_model.create_product(
            "Health Check Test Product", 
            "https://test.example.com/health-check", 
            test_data
        )
        print(f"✅ Create operation successful - Product ID: {product_id}")
        
        # Test Read
        retrieved = product_model.get_product_by_id(product_id)
        if retrieved:
            print("✅ Read operation successful")
        else:
            print("❌ Read operation failed")
            return False
        
        # Test Update
        update_data = {
            "summary": {"Positive": 3, "Negative": 1, "Neutral": 0},
            "reviews": retrieved["reviews"]
        }
        if product_model.update_product_sentiment(product_id, update_data):
            print("✅ Update operation successful")
        else:
            print("❌ Update operation failed")
            return False
        
        # Test Delete
        if product_model.delete_product(product_id):
            print("✅ Delete operation successful")
        else:
            print("❌ Delete operation failed")
            return False
        
        # Test 3: Collection Access
        print("\n3. Testing Collection Access...")
        products = product_model.get_all_products()
        print(f"✅ Products collection accessible - Found {len(products)} existing products")
        
        # Test 4: Database Info
        print("\n4. Database Information...")
        db_stats = db_connection.db.command("dbstats")
        print(f"✅ Database Name: {db_connection.db_name}")
        print(f"✅ Collections: {db_stats.get('collections', 'N/A')}")
        print(f"✅ Data Size: {db_stats.get('dataSize', 'N/A')} bytes")
        
        print("\n🎉 All database tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Database operation failed: {e}")
        return False

def check_configuration():
    print("\n🔧 Configuration Check")
    print("=" * 50)
    
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file exists")
        
        with open(env_file, 'r') as f:
            content = f.read()
            
        if 'MONGODB_CONNECTION_STRING=' in content:
            conn_str = content.split('MONGODB_CONNECTION_STRING=')[1].strip()
            if 'your_username' in conn_str or 'your_password' in conn_str:
                print("❌ Connection string contains placeholder values")
                print("   Please update with actual MongoDB Atlas credentials")
                return False
            else:
                print("✅ Connection string appears configured")
                return True
        else:
            print("❌ MONGODB_CONNECTION_STRING not found in .env")
            return False
    else:
        print("❌ .env file not found")
        print("   Copy .env.example to .env and configure it")
        return False

if __name__ == "__main__":
    print("MongoDB Atlas Database Health Check")
    print("=" * 50)
    
    config_ok = check_configuration()
    
    if config_ok:
        db_ok = check_database_health()
        
        if not db_ok:
            print("\n💡 Quick Fix Steps:")
            print("1. Verify MongoDB Atlas cluster is running")
            print("2. Check network access allows your IP")
            print("3. Ensure database user has correct permissions")
            print("4. Validate connection string format")
    else:
        print("\n💡 Configuration Required:")
        print("1. Copy .env.example to .env")
        print("2. Update with your MongoDB Atlas credentials")
        print("3. Run this script again")
