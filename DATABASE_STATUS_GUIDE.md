# How to Check if MongoDB Database is Working

## Quick Methods to Check Database Status

### 1. **Command Line Health Check** ⚡
```bash
cd /Users/swethas/Downloads/Major\ pr5oject
python check_database.py
```

### 2. **API Endpoint Check** 🌐
```bash
curl http://localhost:5001/database-status
```

### 3. **Web Interface Check** 🖥️
Visit: `http://localhost:5001/database-status` in your browser

### 4. **Manual Backend Logs** 📋
Check the backend console output when starting:
```bash
cd /Users/swethas/Downloads/Major\ pr5oject
python app.py
```
Look for:
- ✅ "Connected to MongoDB Atlas successfully!"
- ❌ "Warning: MongoDB connection string not configured. Running without database."

---

## Understanding the Status Output

### ✅ **Database Working Properly**
```json
{
    "database_connected": true,
    "connection_configured": true,
    "features_available": {
        "store_products": true,
        "retrieve_products": true,
        "search_reviews": true
    },
    "products_stored": 5
}
```

### ❌ **Database Not Configured**
```json
{
    "database_connected": false,
    "connection_configured": false,
    "features_available": {
        "store_products": false,
        "retrieve_products": false,
        "search_reviews": false
    }
}
```

### ⚠️ **Database Configured but Not Connected**
```json
{
    "database_connected": false,
    "connection_configured": true,
    "features_available": {
        "store_products": false,
        "retrieve_products": false,
        "search_reviews": false
    }
}
```

---

## Troubleshooting Steps

### **If Database Not Connected:**

1. **Check .env Configuration**
   ```bash
   cat .env
   ```
   Look for placeholder values like `your_username` or `your_password`

2. **Verify MongoDB Atlas Setup**
   - Cluster is running
   - Network access allows your IP
   - Database user has correct permissions

3. **Test Connection String**
   ```bash
   python -c "
   from pymongo import MongoClient
   from dotenv import load_dotenv
   import os
   load_dotenv()
   try:
       client = MongoClient(os.getenv('MONGODB_CONNECTION_STRING'))
       print('✅ Connection successful')
       client.close()
   except Exception as e:
       print(f'❌ Connection failed: {e}')
   "
   ```

### **If Configuration Issues:**

1. **Update .env File**
   ```bash
   # Edit .env with actual MongoDB Atlas credentials
   MONGODB_CONNECTION_STRING=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/?retryWrites=true&w=majority
   DB_NAME=product_sentiment_db
   ```

2. **Restart Backend**
   ```bash
   # Stop current backend (Ctrl+C)
   # Start again
   python app.py
   ```

---

## Expected Behavior

### **With Database Working:**
- ✅ Products are stored in MongoDB
- ✅ Can retrieve previously analyzed products
- ✅ Search functionality works
- ✅ Data persists between server restarts

### **Without Database:**
- ⚠️ Products are analyzed but not stored
- ⚠️ Cannot retrieve previous analyses
- ⚠️ Search functionality unavailable
- ✅ Basic sentiment analysis still works

---

## Quick Test Commands

### Test Database Operations:
```bash
# 1. Check status
curl http://localhost:5001/database-status

# 2. Test product analysis (will store if DB working)
curl -X POST -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}' \
  http://localhost:5001/analyze-product

# 3. Check if product was stored
curl http://localhost:5001/products
```

### Run Full Health Check:
```bash
python check_database.py
```

---

## Next Steps

1. **If database is working**: Start using the full application features
2. **If database needs setup**: Follow `DATABASE_SETUP.md` instructions
3. **If issues persist**: Check MongoDB Atlas dashboard and network settings
