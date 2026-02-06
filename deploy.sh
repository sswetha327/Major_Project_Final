#!/bin/bash

# Deployment Script for Product Sentiment Analyzer
# Usage: ./deploy.sh [vercel|heroku|railway|vps]

set -e

DEPLOYMENT_TARGET=${1:-vercel}

echo "🚀 Starting deployment to $DEPLOYMENT_TARGET..."
echo "=================================="

# Check if we're in the right directory
if [ ! -f "app.py" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Must be run from project root directory"
    exit 1
fi

# Function to deploy to Vercel
deploy_vercel() {
    echo "📦 Deploying frontend to Vercel..."
    
    cd frontend
    
    # Update API URL for production
    if [ -f "src/App.production.js" ]; then
        echo "🔄 Updating API URL for production..."
        cp src/App.production.js src/App.js
    fi
    
    # Install Vercel CLI if not present
    if ! command -v vercel &> /dev/null; then
        echo "📥 Installing Vercel CLI..."
        npm install -g vercel
    fi
    
    # Deploy
    echo "🚀 Deploying to Vercel..."
    vercel --prod
    
    cd ..
    echo "✅ Frontend deployed to Vercel!"
}

# Function to deploy backend to Railway
deploy_railway() {
    echo "🐍 Deploying backend to Railway..."
    
    # Install Railway CLI if not present
    if ! command -v railway &> /dev/null; then
        echo "📥 Installing Railway CLI..."
        npm install -g @railway/cli
    fi
    
    # Login to Railway
    echo "🔐 Please login to Railway..."
    railway login
    
    # Initialize Railway project
    echo "📋 Initializing Railway project..."
    railway init
    
    # Deploy
    echo "🚀 Deploying to Railway..."
    railway up
    
    echo "✅ Backend deployed to Railway!"
    echo "📝 Don't forget to set environment variables in Railway dashboard:"
    echo "   - MONGODB_CONNECTION_STRING"
    echo "   - DB_NAME"
    echo "   - FLASK_ENV=production"
}

# Function to deploy to Heroku
deploy_heroku() {
    echo "🟣 Deploying to Heroku..."
    
    # Install Heroku CLI if not present
    if ! command -v heroku &> /dev/null; then
        echo "📥 Installing Heroku CLI..."
        brew install heroku/brew/heroku-core/heroku
    fi
    
    # Login to Heroku
    echo "🔐 Please login to Heroku..."
    heroku login
    
    # Create Heroku app
    APP_NAME="sentiment-analyzer-$(date +%s)"
    echo "📱 Creating Heroku app: $APP_NAME"
    heroku create $APP_NAME
    
    # Set environment variables
    echo "⚙️ Setting environment variables..."
    heroku config:set MONGODB_CONNECTION_STRING=$MONGODB_CONNECTION_STRING
    heroku config:set DB_NAME=$DB_NAME
    heroku config:set FLASK_ENV=production
    
    # Deploy
    echo "🚀 Deploying to Heroku..."
    git add .
    git commit -m "Deploy to Heroku"
    heroku git:main
    
    echo "✅ Backend deployed to Heroku!"
}

# Function to prepare for VPS deployment
prepare_vps() {
    echo "🖥 Preparing for VPS deployment..."
    
    # Create deployment package
    echo "📦 Creating deployment package..."
    mkdir -p deployment
    cp -r frontend deployment/
    cp -r database deployment/
    cp -r scraper deployment/
    cp -r sentiment deployment/
    cp app.py deployment/
    cp requirements.txt deployment/
    cp Procfile deployment/
    cp ecosystem.config.js deployment/
    cp .env.production.example deployment/.env.production
    
    # Create setup script
    cat > deployment/setup.sh << 'EOF'
#!/bin/bash
echo "🔧 Setting up Product Sentiment Analyzer..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and Node.js
sudo apt install python3-pip nodejs npm -y

# Install PM2 for process management
npm install -g pm2

# Install dependencies
pip3 install -r requirements.txt
cd frontend && npm install

# Start services with PM2
cd ..
pm2 start ecosystem.config.js

echo "✅ Setup complete!"
echo "🌐 App should be available at http://your-server-ip:3000"
EOF
    
    chmod +x deployment/setup.sh
    
    # Create deployment instructions
    cat > deployment/README.md << 'EOF'
# VPS Deployment Instructions

1. Copy deployment folder to your VPS:
   scp -r deployment/ user@your-server:/home/user/

2. SSH into your VPS:
   ssh user@your-server

3. Run setup script:
   cd deployment
   ./setup.sh

4. Configure environment:
   cp .env.production .env
   # Edit .env with your actual values

5. Start services:
   pm2 start ecosystem.config.js

6. Setup reverse proxy (nginx):
   sudo apt install nginx -y
   # Configure nginx to proxy port 3000 and 5001
EOF
    
    echo "✅ VPS deployment package created in deployment/ folder"
}

# Main deployment logic
case $DEPLOYMENT_TARGET in
    vercel)
        deploy_vercel
        ;;
    railway)
        deploy_railway
        ;;
    heroku)
        deploy_heroku
        ;;
    vps)
        prepare_vps
        ;;
    *)
        echo "❌ Unknown deployment target: $DEPLOYMENT_TARGET"
        echo "Usage: ./deploy.sh [vercel|heroku|railway|vps]"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment process completed!"
echo ""
echo "📋 Next steps:"
echo "1. Set environment variables in deployment platform"
echo "2. Test your deployed application"
echo "3. Configure custom domain (optional)"
echo "4. Set up monitoring and analytics"
echo ""
echo "📚 For detailed instructions, see DEPLOYMENT_GUIDE.md"
