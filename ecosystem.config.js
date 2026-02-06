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
        MONGODB_CONNECTION_STRING: 'your-mongo-atlas-uri',
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
