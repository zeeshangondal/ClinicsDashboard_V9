# Craft AI Dashboard - Deployment Guide

**Version**: 2.1.0 (Login Fix Update)  
**Last Updated**: July 23, 2025

## 🎯 Overview

This guide provides comprehensive instructions for deploying the Craft AI Dashboard with the latest login fixes and enhancements. The application now includes automatic demo account creation and a refined user interface.

## 🚀 Quick Deployment (Recommended)

### Live Application
The application is already deployed and ready to use:
- **URL**: https://y0h0i3cqj1eo.manus.space
- **Demo Login**: Demo Clinic / demo / demo
- **Super Admin**: craft_admin / CraftAI2024!

### Manus Platform Deployment
```bash
# Clone or extract the deployment package
cd craft-ai-dashboard-final-deployment

# Deploy to Manus platform
manus deploy backend --framework flask --project-dir .
```

The deployment will automatically:
- ✅ Create database tables
- ✅ Initialize super admin account
- ✅ Create demo clinic and user
- ✅ Serve the React frontend
- ✅ Enable CORS for API access

## 📋 Pre-Deployment Checklist

### System Requirements
- **Python**: 3.11 or higher
- **Node.js**: 18 or higher (for frontend development)
- **Memory**: Minimum 512MB RAM
- **Storage**: At least 1GB available space
- **Network**: Internet access for package installation

### Environment Preparation
1. **Verify Python Installation**
   ```bash
   python3 --version  # Should show 3.11+
   pip3 --version     # Should be available
   ```

2. **Check Dependencies**
   ```bash
   # All required packages are listed in requirements.txt
   cat requirements.txt
   ```

3. **Environment Variables** (Optional)
   ```bash
   # Create .env file if needed
   cp .env.example .env
   # Edit .env with your specific configuration
   ```

## 🛠 Deployment Methods

### Method 1: Manus Platform (Recommended)

**Advantages:**
- Automatic HTTPS/SSL
- Built-in monitoring
- Easy scaling
- Automatic backups

**Steps:**
```bash
# 1. Prepare the project
cd craft-ai-dashboard-final-deployment

# 2. Deploy
manus deploy backend --framework flask --project-dir .

# 3. Access your application
# URL will be provided after successful deployment
```

**Expected Output:**
```
✅ Building application...
✅ Installing dependencies...
✅ Starting Flask server...
✅ Database initialized successfully
✅ Super admin created: craft_admin / CraftAI2024!
✅ Demo Clinic created
✅ Demo user created
🌐 Application deployed to: https://[your-unique-url].manus.space
```

### Method 2: Docker Deployment

**Prerequisites:**
- Docker installed
- Docker Compose installed

**Steps:**
```bash
# 1. Create docker-compose.yml
cat > docker-compose.yml << EOF
version: '3.8'
services:
  craft-ai-dashboard:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:///craft_ai.db
    volumes:
      - ./data:/app/data
    restart: unless-stopped
EOF

# 2. Create Dockerfile
cat > Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
EOF

# 3. Deploy
docker-compose up --build -d

# 4. Check status
docker-compose logs -f
```

### Method 3: Manual Server Deployment

**For VPS/Dedicated Server:**

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python and dependencies
sudo apt install python3 python3-pip python3-venv -y

# 3. Create application directory
sudo mkdir -p /opt/craft-ai-dashboard
sudo chown $USER:$USER /opt/craft-ai-dashboard

# 4. Copy application files
cp -r craft-ai-dashboard-final-deployment/* /opt/craft-ai-dashboard/

# 5. Create virtual environment
cd /opt/craft-ai-dashboard
python3 -m venv venv
source venv/bin/activate

# 6. Install dependencies
pip install -r requirements.txt

# 7. Create systemd service
sudo tee /etc/systemd/system/craft-ai-dashboard.service << EOF
[Unit]
Description=Craft AI Dashboard
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/craft-ai-dashboard
Environment=PATH=/opt/craft-ai-dashboard/venv/bin
ExecStart=/opt/craft-ai-dashboard/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 8. Start service
sudo systemctl daemon-reload
sudo systemctl enable craft-ai-dashboard
sudo systemctl start craft-ai-dashboard

# 9. Check status
sudo systemctl status craft-ai-dashboard
```

### Method 4: Cloud Platform Deployment

#### Heroku Deployment
```bash
# 1. Install Heroku CLI
# 2. Login to Heroku
heroku login

# 3. Create application
heroku create craft-ai-dashboard-[your-name]

# 4. Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(16))')

# 5. Deploy
git init
git add .
git commit -m "Initial deployment"
git push heroku main
```

#### AWS EC2 Deployment
```bash
# 1. Launch EC2 instance (Ubuntu 22.04)
# 2. Connect via SSH
ssh -i your-key.pem ubuntu@your-ec2-ip

# 3. Follow Manual Server Deployment steps above
# 4. Configure security groups for port 5000
# 5. Optional: Set up Nginx reverse proxy
```

## 🔧 Configuration Options

### Environment Variables

Create `.env` file with the following variables:

```bash
# Application Settings
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
DEBUG=False

# Database Configuration
DATABASE_URL=sqlite:///craft_ai.db
# For PostgreSQL: postgresql://user:password@localhost/craft_ai

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=900  # 15 minutes
JWT_REFRESH_TOKEN_EXPIRES=604800  # 7 days

# CORS Settings
CORS_ORIGINS=*
# For production: https://yourdomain.com,https://app.yourdomain.com

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# WhatsApp API (Optional)
WHATSAPP_API_URL=https://api.whatsapp.com
WHATSAPP_API_TOKEN=your-whatsapp-token

# SMS Configuration (Optional)
SMS_PROVIDER=twilio
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890
```

### Database Configuration

#### SQLite (Default - Development)
```python
DATABASE_URL=sqlite:///craft_ai.db
```

#### PostgreSQL (Recommended - Production)
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Create database and user
sudo -u postgres psql
CREATE DATABASE craft_ai;
CREATE USER craft_ai_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE craft_ai TO craft_ai_user;
\q

# Update environment variable
DATABASE_URL=postgresql://craft_ai_user:secure_password@localhost/craft_ai
```

#### MySQL (Alternative)
```bash
# Install MySQL
sudo apt install mysql-server -y

# Create database and user
sudo mysql
CREATE DATABASE craft_ai;
CREATE USER 'craft_ai_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON craft_ai.* TO 'craft_ai_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Update environment variable
DATABASE_URL=mysql://craft_ai_user:secure_password@localhost/craft_ai
```

## 🔐 Security Configuration

### SSL/HTTPS Setup (Nginx)

```bash
# 1. Install Nginx
sudo apt install nginx -y

# 2. Create Nginx configuration
sudo tee /etc/nginx/sites-available/craft-ai-dashboard << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# 3. Enable site
sudo ln -s /etc/nginx/sites-available/craft-ai-dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 4. Install SSL certificate (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### Firewall Configuration

```bash
# Enable UFW firewall
sudo ufw enable

# Allow SSH
sudo ufw allow ssh

# Allow HTTP and HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Allow application port (if not using Nginx)
sudo ufw allow 5000

# Check status
sudo ufw status
```

## 📊 Monitoring & Maintenance

### Health Check Endpoint
The application provides a health check endpoint:
```
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "message": "Craft AI Dashboard API is running"
}
```

### Log Monitoring

```bash
# Application logs (systemd)
sudo journalctl -u craft-ai-dashboard -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Application-specific logs
tail -f /opt/craft-ai-dashboard/logs/app.log
```

### Database Backup

```bash
# SQLite backup
cp /opt/craft-ai-dashboard/craft_ai.db /backup/craft_ai_$(date +%Y%m%d_%H%M%S).db

# PostgreSQL backup
pg_dump -U craft_ai_user craft_ai > /backup/craft_ai_$(date +%Y%m%d_%H%M%S).sql
```

### Automated Backup Script

```bash
#!/bin/bash
# Create backup script
cat > /opt/craft-ai-dashboard/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backup/craft-ai"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
cp /opt/craft-ai-dashboard/craft_ai.db $BACKUP_DIR/craft_ai_$DATE.db

# Keep only last 7 days of backups
find $BACKUP_DIR -name "craft_ai_*.db" -mtime +7 -delete

echo "Backup completed: craft_ai_$DATE.db"
EOF

# Make executable
chmod +x /opt/craft-ai-dashboard/backup.sh

# Add to crontab (daily backup at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/craft-ai-dashboard/backup.sh") | crontab -
```

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. Login Failed Error
**Status**: ✅ **RESOLVED in v2.1.0**
- Demo accounts are now created automatically
- No manual intervention required

#### 2. Database Connection Error
```bash
# Check database file permissions
ls -la craft_ai.db
chmod 664 craft_ai.db

# Check database connectivity
python3 -c "
from src.main import app
from src.models.user import db
with app.app_context():
    print('Database connection:', db.engine.url)
"
```

#### 3. Port Already in Use
```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill process if needed
sudo kill -9 <PID>

# Or use different port
export PORT=5001
python app.py
```

#### 4. Permission Denied Errors
```bash
# Fix file permissions
sudo chown -R $USER:$USER /opt/craft-ai-dashboard
chmod -R 755 /opt/craft-ai-dashboard
```

#### 5. Module Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Clear Python cache
find . -type d -name __pycache__ -delete
find . -name "*.pyc" -delete
```

### Performance Optimization

#### 1. Database Optimization
```python
# Add database indexes (in production)
# Edit src/models/*.py to add indexes
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    # ... other fields
```

#### 2. Caching Configuration
```python
# Add Redis caching (optional)
pip install redis flask-caching

# In src/config.py
CACHE_TYPE = "redis"
CACHE_REDIS_URL = "redis://localhost:6379/0"
```

#### 3. Production WSGI Server
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app

# Update systemd service
ExecStart=/opt/craft-ai-dashboard/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Implement session storage (Redis)
- Database connection pooling
- CDN for static assets

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Enable caching layers
- Monitor resource usage

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# 1. Backup current installation
cp -r /opt/craft-ai-dashboard /opt/craft-ai-dashboard.backup

# 2. Stop the service
sudo systemctl stop craft-ai-dashboard

# 3. Update code
cd /opt/craft-ai-dashboard
git pull origin main  # or copy new files

# 4. Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# 5. Run database migrations (if any)
python -c "
from src.main import app
from src.models.user import db
with app.app_context():
    db.create_all()
"

# 6. Start the service
sudo systemctl start craft-ai-dashboard
```

## 📞 Support and Resources

### Getting Help
- **Documentation**: Check `/docs/` directory
- **Logs**: Monitor application and system logs
- **Health Check**: Use `/api/health` endpoint
- **Database**: Verify demo accounts exist

### Useful Commands
```bash
# Check application status
curl -s http://localhost:5000/api/health | jq

# Test login API
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"clinic_name":"Demo Clinic","username":"demo","password":"demo"}'

# Monitor real-time logs
sudo journalctl -u craft-ai-dashboard -f

# Check database contents
python3 -c "
from src.main import app
from src.models.user import User
from src.models.clinic import Clinic
with app.app_context():
    print('Clinics:', [c.name for c in Clinic.query.all()])
    print('Users:', [u.username for u in User.query.all()])
"
```

---

**🎯 Deployment Complete**: Your Craft AI Dashboard is now ready for production use with automatic demo account creation and all the latest enhancements!

