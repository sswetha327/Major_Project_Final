import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.connection_string = os.getenv('MONGODB_CONNECTION_STRING')
        self.db_name = os.getenv('DB_NAME', 'product_sentiment_db')
        self.client = None
        self.db = None
        self.connected = False
    
    def connect(self):
        # Check if connection string is properly configured
        if not self.connection_string or 'your_username' in self.connection_string:
            print("Warning: MongoDB connection string not configured. Running without database.")
            self.connected = False
            return False
        
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.db_name]
            self.connected = True
            print("Connected to MongoDB Atlas successfully!")
            return True
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            print("Running without database connection.")
            self.connected = False
            return False
    
    def disconnect(self):
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")
    
    def get_collection(self, collection_name):
        if not self.connected or self.db is None:
            raise Exception("Database not connected. Check your MongoDB configuration.")
        return self.db[collection_name]
    
    def is_connected(self):
        return self.connected

db_connection = DatabaseConnection()
