# Deployment Guide for Product Sentiment Analyzer

## Current Development Setup
- **Backend**: Flask app running on localhost:5001
- **Frontend**: React app running on localhost:3000
- **Database**: MongoDB Atlas (cloud-based)
- **State**: Development mode

## Deployment Options

### Option 1: Vercel + Railway (Recommended for Beginners)
**Frontend (Vercel)**:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy frontend
cd frontend
vercel --prod
```

**Backend (Railway)**:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy backend
railway login
railway init
railway up
```

### Option 2: Heroku (Free Tier)
```bash
# Install Heroku CLI
brew install heroku/brew/heroku-core/heroku

# Deploy backend
heroku create your-app-name
heroku config:set MONGODB_CONNECTION_STRING="your-mongo-uri"
heroku config:set DB_NAME="your-db-name"
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Option 3: AWS/Azure/GCP (Production)
More complex, requires Docker configuration and cloud setup.

### Option 4: Self-Hosted VPS (Full Control)
```bash
# On your VPS (Ubuntu example)
sudo apt update
sudo apt install python3-pip nodejs npm

# Clone and setup
git clone your-repo
cd your-repo
pip install -r requirements.txt
cd frontend && npm install

# Setup process managers (PM2)
npm install -g pm2
pm2 start ecosystem.config.js
```

## Pre-Deployment Checklist

### Backend Changes Needed:
1. **Environment Variables**:
   - Set production MongoDB connection string
   - Configure CORS for production domain
   - Set proper Flask secret key

2. **Security**:
   - Add input validation
   - Rate limiting
   - HTTPS enforcement

3. **Performance**:
   - Add caching
   - Optimize database queries
   - Compress responses

### Frontend Changes Needed:
1. **API URL**:
   - Update from localhost to production URL
   - Add error handling for network issues

2. **Build Optimization**:
   - Minimize bundle size
   - Optimize images
   - Add service worker

## Quick Deploy (Vercel + Railway)

### Step 1: Prepare Frontend
```bash
cd frontend
# Update API URL in App.js
sed -i 's/http:\/\/127.0.0.1:5001/https:\/\/your-backend-url.vercel.app/g' src/App.js

# Deploy to Vercel
npm run build
vercel --prod
```

### Step 2: Prepare Backend
```bash
# Create requirements.txt for production
pip freeze > requirements.txt

# Create Procfile for Railway
echo "web: python app.py" > Procfile

# Deploy to Railway
railway login
railway init
railway up
```

### Step 3: Configure Environment
```bash
# On Railway dashboard, add:
MONGODB_CONNECTION_STRING=your-mongo-atlas-uri
DB_NAME=your-db-name
FLASK_ENV=production
```

## Production Configuration Files

### Railway Procfile
```
web: python app.py
```

### Vercel vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": { "distDir": "build" }
    }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "/index.html" }
  ]
}
```

### PM2 Ecosystem (for VPS)
```javascript
module.exports = {
  apps: [
    {
      name: 'sentiment-backend',
      script: 'app.py',
      interpreter: 'python3',
      cwd: '/path/to/your/app',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        MONGODB_CONNECTION_STRING: 'your-mongo-uri',
        DB_NAME: 'your-db-name'
      }
    },
    {
      name: 'sentiment-frontend',
      script: 'npm start',
      cwd: '/path/to/your/frontend',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G'
    }
  ]
};
```

## Deployment Steps

### 1. Choose Your Platform
- **Beginner**: Vercel + Railway (Free, easy)
- **Intermediate**: Heroku (Free tier, moderate complexity)
- **Advanced**: AWS/Azure/GCP (Full control, complex)
- **Self-hosted**: VPS (Maximum control, requires maintenance)

### 2. Prepare Your Code
- Update environment variables
- Configure CORS for production domain
- Add production optimizations
- Create deployment configuration files

### 3. Deploy
- Push to Git
- Connect deployment platform
- Configure environment variables
- Test deployment

### 4. Post-Deployment
- Test all functionality
- Monitor logs
- Set up domain
- Configure SSL (if needed)

## Cost Estimates

### Free Tier Options:
- **Vercel**: $0-20/month (hobby)
- **Railway**: $0-5/month (hobby)
- **Heroku**: $0-7/month (eco dyno)
- **MongoDB Atlas**: Free tier (512MB)

### Paid Options:
- **VPS**: $5-20/month (DigitalOcean, Linode)
- **AWS**: $10-50/month (depending on usage)
- **Azure**: $10-40/month (depending on services)

## Security Considerations

### Must-Have:
1. **HTTPS**: SSL certificates
2. **Environment Variables**: Never commit secrets
3. **Input Validation**: Sanitize all inputs
4. **Rate Limiting**: Prevent abuse
5. **CORS**: Restrict to your domain only

### Recommended:
1. **Monitoring**: Error tracking, uptime
2. **Backup**: Database and code backups
3. **CDN**: For static assets
4. **Analytics**: Usage monitoring

## Next Steps

1. **Choose deployment platform** based on your budget and technical skills
2. **Prepare code** with production configurations
3. **Test locally** one final time
4. **Deploy** following platform-specific instructions
5. **Monitor** and maintain the deployment

Would you like me to help you with any specific deployment option?
