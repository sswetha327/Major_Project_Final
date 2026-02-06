# MongoDB Atlas Setup Instructions

## 1. Create MongoDB Atlas Account
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up for a free account
3. Create a new project

## 2. Create a Cluster
1. Click "Build a Cluster"
2. Choose "M0 Sandbox" (free tier)
3. Select a cloud provider and region closest to you
4. Leave cluster name as default or customize it
5. Click "Create Cluster"

## 3. Configure Network Access
1. Go to "Network Access" in the left sidebar
2. Click "Add IP Address"
3. Select "Allow Access from Anywhere" (0.0.0.0/0) for development
4. Click "Confirm"

## 4. Create Database User
1. Go to "Database Access" in the left sidebar
2. Click "Add New Database User"
3. Enter username and password (save these credentials)
4. Grant read/write permissions to your database
5. Click "Add User"

## 5. Get Connection String
1. Go to "Clusters" → Click "Connect" on your cluster
2. Select "Connect your application"
3. Copy the connection string
4. Replace `<password>` with your database user password

## 6. Set Up Environment Variables
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your MongoDB credentials:
   ```
   MONGODB_CONNECTION_STRING=mongodb+srv://your_username:your_password@your_cluster.mongodb.net/?retryWrites=true&w=majority
   DB_NAME=product_sentiment_db
   ```

## 7. Install Dependencies
```bash
pip install -r requirements.txt
```

## 8. Test Connection
Run the Flask application:
```bash
python app.py
```

If everything is set up correctly, you should see "Connected to MongoDB Atlas successfully!" in the console.

## Database Schema

### Products Collection
```json
{
  "_id": ObjectId,
  "product_name": "string",
  "product_url": "string",
  "created_at": Date,
  "updated_at": Date,
  "sentiment_summary": {
    "Positive": number,
    "Negative": number,
    "Neutral": number
  },
  "total_reviews": number,
  "reviews": [
    {
      "text": "string",
      "sentiment": "Positive|Negative|Neutral"
    }
  ]
}
```

## API Endpoints

- `POST /analyze-product` - Analyze product and store in database
- `GET /products` - Get all products
- `GET /products/<product_id>` - Get specific product
- `GET /reviews/sentiment/<sentiment>` - Get reviews by sentiment
- `GET /reviews/search?q=<query>` - Search reviews by text
- `DELETE /products/<product_id>` - Delete product
