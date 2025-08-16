# Craft AI Dashboard - Deployment Guide

This guide provides comprehensive instructions for deploying the Craft AI Dashboard in various environments.

## 🚀 Quick Start Options

### Option 1: Docker Deployment (Recommended)

#### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- 2GB RAM minimum, 4GB recommended
- 10GB disk space

#### Steps
```bash
# 1. Extract deployment package
unzip craft-ai-dashboard-fixed-deployment.zip
cd craft-ai-dashboard-fixed-deployment

# 2. Configure environment (optional)
cp .env.example .env
# Edit .env with your preferred settings

# 3. Build and start services
docker-compose up --build -d

# 4. Verify deployment
curl http://localhost:5000/health

# 5. Access application
open http://localhost:5000
```

#### Docker Commands Reference
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f craft-ai-dashboard

# Restart services
docker-compose restart

# Update application
docker-compose down
docker-compose up --build -d
```

### Option 2: Manual Installation

#### Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend development)
- SQLite3 (or PostgreSQL/MySQL)

#### Backend Setup
```bash
# 1. Navigate to project directory
cd craft-ai-dashboard-fixed-deployment

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env file with your settings

# 5. Initialize database
python -c "from src.main import app, db; app.app_context().push(); db.create_all()"

# 6. Start application
python app.py
```

#### Frontend Development (Optional)
```bash
# 1. Navigate to frontend source
cd frontend_src

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev

# 4. Build for production
npm run build

# 5. Copy built files to backend
cp -r dist/* ../src/static/
```

### Option 3: Production Server Deployment

#### Using Gunicorn (Recommended)
```bash
# Install Gunicorn
pip install gunicorn eventlet

# Start with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class eventlet app:app

# With configuration file
gunicorn --config gunicorn.conf.py app:app
```

#### Gunicorn Configuration (`gunicorn.conf.py`)
```python
bind = "0.0.0.0:5000"
workers = 4
worker_class = "eventlet"
worker_connections = 1000
timeout = 120
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

#### Using Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /socket.io/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🗄️ Database Configuration

### SQLite (Default)
```env
DATABASE_URL=sqlite:///craft_ai.db
```

### PostgreSQL
```env
DATABASE_URL=postgresql://username:password@localhost/craft_ai
```

#### PostgreSQL Setup
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE craft_ai;
CREATE USER craft_ai_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE craft_ai TO craft_ai_user;
\q
```

### MySQL
```env
DATABASE_URL=mysql://username:password@localhost/craft_ai
```

## 🔒 Security Configuration

### SSL/HTTPS Setup
```bash
# Generate SSL certificate (Let's Encrypt)
sudo certbot --nginx -d your-domain.com

# Or use self-signed certificate for testing
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

### Environment Security
```env
# Use strong, unique keys
JWT_SECRET_KEY=$(openssl rand -base64 32)
SECRET_KEY=$(openssl rand -base64 32)

# Restrict CORS origins
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Enable security headers
FLASK_ENV=production
FLASK_DEBUG=False
```

### Firewall Configuration
```bash
# Allow HTTP and HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Allow SSH (if needed)
sudo ufw allow 22

# Enable firewall
sudo ufw enable
```

## 🌐 Cloud Deployment

### AWS EC2
```bash
# 1. Launch EC2 instance (Ubuntu 22.04 LTS)
# 2. Connect via SSH
ssh -i your-key.pem ubuntu@your-ec2-ip

# 3. Update system
sudo apt update && sudo apt upgrade -y

# 4. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# 5. Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 6. Deploy application
scp -i your-key.pem craft-ai-dashboard-fixed-deployment.zip ubuntu@your-ec2-ip:~/
ssh -i your-key.pem ubuntu@your-ec2-ip
unzip craft-ai-dashboard-fixed-deployment.zip
cd craft-ai-dashboard-fixed-deployment
docker-compose up -d
```

### Google Cloud Platform
```bash
# Using Google Cloud Run
gcloud run deploy craft-ai-dashboard \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### DigitalOcean
```bash
# Using DigitalOcean App Platform
doctl apps create --spec app-spec.yaml
```

## 📊 Monitoring & Logging

### Application Logs
```bash
# View logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f craft-ai-dashboard
```

### Health Monitoring
```bash
# Health check endpoint
curl http://localhost:5000/health

# System metrics
curl http://localhost:5000/metrics
```

### Log Rotation
```bash
# Configure logrotate
sudo nano /etc/logrotate.d/craft-ai-dashboard

/path/to/craft-ai-dashboard/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 craftai craftai
    postrotate
        systemctl reload craft-ai-dashboard
    endscript
}
```

## 🔄 Backup & Recovery

### Database Backup
```bash
# SQLite backup
cp craft_ai.db backup_$(date +%Y%m%d_%H%M%S).db

# PostgreSQL backup
pg_dump craft_ai > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Automated Backup Script
```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
cp /app/data/craft_ai.db $BACKUP_DIR/craft_ai_$DATE.db

# Backup application files
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /app

# Clean old backups (keep 30 days)
find $BACKUP_DIR -name "*.db" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Login Fields Not Clickable
**Status**: ✅ FIXED in this version
**Solution**: Updated CSS with proper z-index and pointer-events

#### 2. Database Connection Error
```bash
# Check database file permissions
ls -la craft_ai.db
sudo chown craftai:craftai craft_ai.db

# Verify database URL
echo $DATABASE_URL
```

#### 3. Port Already in Use
```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill process
sudo kill -9 <PID>

# Or use different port
export PORT=8000
```

#### 4. CORS Errors
```env
# Update CORS settings in .env
CORS_ORIGINS=*
# Or specify allowed origins
CORS_ORIGINS=https://yourdomain.com,http://localhost:3000
```

#### 5. Memory Issues
```bash
# Check memory usage
free -h

# Increase swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Performance Optimization

#### 1. Database Optimization
```sql
-- Create indexes for better performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
```

#### 2. Caching
```env
# Enable Redis caching
REDIS_URL=redis://localhost:6379/0
```

#### 3. Static File Serving
```nginx
# Serve static files with Nginx
location /static/ {
    alias /app/src/static/;
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## 📞 Support

### Getting Help
1. Check this deployment guide
2. Review error logs
3. Consult API documentation
4. Check system requirements

### System Requirements
- **Minimum**: 2GB RAM, 2 CPU cores, 10GB storage
- **Recommended**: 4GB RAM, 4 CPU cores, 20GB storage
- **Operating System**: Ubuntu 20.04+, CentOS 8+, or Docker-compatible OS

---

**Last Updated**: January 2025  
**Version**: 2.1.0 (Fixed Login Issue)

