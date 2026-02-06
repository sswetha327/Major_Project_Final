# How to Check Stored URLs in Database

## **Quick Methods to Check Stored URLs**

### 1. **Command Line Tool** ⚡
```bash
python check_stored_urls.py
```
This shows:
- ✅ All stored products with URLs
- 📅 Creation dates
- 📈 Review counts and sentiment summaries
- 🎯 Database IDs

### 2. **Web API Endpoint** 🌐
```bash
curl http://localhost:5001/products
```
Returns JSON with all stored products and their URLs.

### 3. **Browser Access** 🖥️
Visit: `http://localhost:5001/products` in your browser

### 4. **Check Specific URL** 🔍
```bash
# Modify check_stored_urls.py to check your specific URL
check_specific_url("your-url-here")
```

---

## **What You'll See**

### **Stored Products Example:**
```
📊 Found 5 stored products:

1. **Product**: Unknown Product
   🔗 **URL**: https://example.com/test-product
   📅 **Created**: 2026-02-05 07:52:55.782000
   📈 **Reviews**: 20 total
   🎯 **Sentiment Summary**: {'Positive': 4, 'Negative': 10, 'Neutral': 6}
   🆔 **Database ID**: 69844c57a10825db2cbca60a

2. **Product**: Unknown Product
   🔗 **URL**: https://www.amazon.com/test-product
   📅 **Created**: 2026-02-05 07:59:30.236000
   📈 **Reviews**: 20 total
   🎯 **Sentiment Summary**: {'Positive': 4, 'Negative': 10, 'Neutral': 6}
   🆔 **Database ID**: 69844de2e7db0b0fe3b056d3
```

### **URL Check Results:**
- ✅ **URL Found**: Shows product details and sample reviews
- ❌ **URL Not Found**: Means the URL hasn't been analyzed yet

---

## **Current Stored URLs**

Based on the database check, you currently have **5 stored URLs**:

1. ✅ `https://example.com/test-product` - **Found**
2. ✅ `https://example.com` - **Found**  
3. ✅ `https://example.com/test` - **Found**
4. ✅ `https://www.amazon.com/test-product` - **Found**
5. ✅ `https://www.myntra.com/mailers/watches/...` - **Found**

---

## **Database Statistics**

- **Total Products**: 5
- **Total Reviews Analyzed**: 100
- **Overall Sentiment**:
  - 😊 Positive: 20
  - 😠 Negative: 48  
  - 😐 Neutral: 32

---

## **How to Verify New URLs**

When you analyze a new URL in the website:

1. **Analyze the URL** in the frontend (`http://localhost:3004`)
2. **Check if stored**:
   ```bash
   python check_stored_urls.py
   ```
3. **Look for your URL** in the output
4. **Or check specifically**:
   ```bash
   # Add this to the script and run
   check_specific_url("your-new-url")
   ```

---

## **Real-time Verification**

The system automatically:
- ✅ **Checks for duplicates** before analyzing
- ✅ **Returns existing data** if URL already analyzed
- ✅ **Stores new analysis** if URL is new
- ✅ **Updates timestamps** on re-analysis

So every URL you enter in the website is **automatically tracked** in the database!
