# Craft AI Dashboard - Deployment Guide

**Version**: 2.2.0 (Outbound Calls Enhancement Update)  
**Last Updated**: January 2025

## 🎯 Overview

This guide provides comprehensive instructions for deploying the Craft AI Dashboard v2.2.0, which includes the latest enhancements to the Outbound Calls module with call type filtering and universal header panels.

## 🚀 Quick Deployment (Recommended)

### **Manus Platform Deployment**

The fastest and most reliable way to deploy the Craft AI Dashboard:

1. **Upload Package**
   ```bash
   # Extract the deployment package
   unzip craft-ai-dashboard-v2.2-final-deployment.zip
   ```

2. **Deploy to Manus**
   - Upload the entire `craft-ai-dashboard-v2.2-final-deployment` folder
   - Select "Flask" as the framework
   - Click "Deploy"
   - Wait for deployment completion

3. **Access Application**
   - Use the provided Manus URL
   - Login with demo credentials: Demo Clinic / demo / demo

### **Expected Result**
- ✅ Fully functional dashboard with all modules
- ✅ Working login and authentication
- ✅ Enhanced Outbound Calls with call type filtering
- ✅ Universal header panels on all modules

## 🛠 Alternative Deployment Methods

### **1. Local Development Setup**

For development and testing purposes:

```bash
# Navigate to project directory
cd craft-ai-dashboard-v2.2-final-deployment

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Access at http://localhost:5000
```

### **2. Docker Deployment**

For containerized deployment:

```bash
# Build Docker image
docker build -t craft-ai-dashboard:v2.2.0 .

# Run container
docker run -d \
  --name craft-ai-dashboard \
  -p 5000:5000 \
  craft-ai-dashboard:v2.2.0

# Access at http://localhost:5000
```

### **3. Production Server Deployment**

For production environments:

```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# Setup application
cd /opt
sudo git clone <repository> craft-ai-dashboard
cd craft-ai-dashboard
sudo python3 -m venv venv
sudo venv/bin/pip install -r requirements.txt

# Configure systemd service
sudo nano /etc/systemd/system/craft-ai-dashboard.service
```

**Service Configuration:**
```ini
[Unit]
Description=Craft AI Dashboard
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/craft-ai-dashboard
Environment=PATH=/opt/craft-ai-dashboard/venv/bin
ExecStart=/opt/craft-ai-dashboard/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl daemon-reload
sudo systemctl enable craft-ai-dashboard
sudo systemctl start craft-ai-dashboard
```

## 🔧 Configuration

### **Environment Variables**

Create a `.env` file for configuration:

```env
# Application Settings
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///craft_ai.db

# Security Settings
JWT_SECRET_KEY=your-jwt-secret-here
JWT_ACCESS_TOKEN_EXPIRES=3600

# CORS Settings
CORS_ORIGINS=*

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

### **Database Configuration**

The application uses SQLite by default with automatic initialization:

```python
# Database is automatically created on first run
# Demo data is seeded automatically
# No manual database setup required
```

### **Frontend Configuration**

The frontend is pre-built and included in the `src/static/` directory:

- ✅ React application built with Vite
- ✅ Optimized for production
- ✅ All assets included
- ✅ No additional build steps required

## 🌐 Cloud Platform Deployment

### **AWS Deployment**

Using AWS Elastic Beanstalk:

1. **Prepare Application**
   ```bash
   # Create application.py (required by EB)
   cp app.py application.py
   
   # Create .ebextensions/python.config
   mkdir .ebextensions
   echo "option_settings:
     aws:elasticbeanstalk:container:python:
       WSGIPath: application.py" > .ebextensions/python.config
   ```

2. **Deploy**
   ```bash
   # Install EB CLI
   pip install awsebcli
   
   # Initialize and deploy
   eb init craft-ai-dashboard
   eb create production
   eb deploy
   ```

### **Google Cloud Platform**

Using Google App Engine:

1. **Create app.yaml**
   ```yaml
   runtime: python39
   
   env_variables:
     FLASK_ENV: production
   
   handlers:
   - url: /static
     static_dir: src/static
   - url: /.*
     script: auto
   ```

2. **Deploy**
   ```bash
   gcloud app deploy
   ```

### **Microsoft Azure**

Using Azure App Service:

1. **Create requirements.txt** (already included)
2. **Deploy via Azure CLI**
   ```bash
   az webapp up --name craft-ai-dashboard --resource-group myResourceGroup
   ```

## 🔐 Security Configuration

### **Production Security Checklist**

- [ ] **Change Default Passwords**
  ```python
  # Update in src/main.py
  SUPER_ADMIN_PASSWORD = "your-secure-password"
  ```

- [ ] **Configure HTTPS**
  ```nginx
  # Nginx SSL configuration
  server {
      listen 443 ssl;
      ssl_certificate /path/to/certificate.crt;
      ssl_certificate_key /path/to/private.key;
  }
  ```

- [ ] **Set Strong Secret Keys**
  ```env
  SECRET_KEY=your-very-long-random-secret-key
  JWT_SECRET_KEY=another-very-long-random-secret-key
  ```

- [ ] **Configure CORS Properly**
  ```python
  # In production, specify exact origins
  CORS_ORIGINS = ["https://yourdomain.com"]
  ```

- [ ] **Enable Rate Limiting**
  ```python
  # Add to requirements.txt: Flask-Limiter
  # Configure in app.py
  ```

## 📊 Monitoring & Logging

### **Application Monitoring**

```python
# Built-in logging configuration
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### **Health Check Endpoint**

```bash
# Check application health
curl http://your-domain/api/health

# Expected response
{
  "status": "healthy",
  "version": "2.2.0",
  "timestamp": "2025-01-23T10:47:55Z"
}
```

### **Performance Monitoring**

```bash
# Monitor resource usage
htop
iostat -x 1
netstat -tuln
```

## 🔄 Updates & Maintenance

### **Updating the Application**

1. **Backup Current Version**
   ```bash
   cp -r craft-ai-dashboard craft-ai-dashboard-backup
   ```

2. **Deploy New Version**
   ```bash
   # Replace files with new version
   # Restart application
   sudo systemctl restart craft-ai-dashboard
   ```

3. **Verify Update**
   ```bash
   # Check version in browser
   # Test core functionality
   # Verify new features
   ```

### **Database Backup**

```bash
# Backup SQLite database
cp src/craft_ai.db backups/craft_ai_$(date +%Y%m%d_%H%M%S).db

# Automated backup script
#!/bin/bash
BACKUP_DIR="/opt/backups"
DB_FILE="/opt/craft-ai-dashboard/src/craft_ai.db"
DATE=$(date +%Y%m%d_%H%M%S)
cp "$DB_FILE" "$BACKUP_DIR/craft_ai_$DATE.db"
find "$BACKUP_DIR" -name "craft_ai_*.db" -mtime +7 -delete
```

## 🐛 Troubleshooting

### **Common Issues**

1. **Application Won't Start**
   ```bash
   # Check logs
   tail -f app.log
   
   # Check port availability
   netstat -tuln | grep 5000
   
   # Check Python dependencies
   pip list
   ```

2. **Database Issues**
   ```bash
   # Reset database (WARNING: Deletes all data)
   rm src/craft_ai.db
   python app.py  # Will recreate with demo data
   ```

3. **Frontend Not Loading**
   ```bash
   # Check static files
   ls -la src/static/
   
   # Verify file permissions
   chmod -R 644 src/static/
   ```

4. **Login Issues**
   ```bash
   # Verify demo credentials in browser console
   # Check authentication logs
   grep "login" app.log
   ```

### **Performance Issues**

1. **Slow Response Times**
   ```bash
   # Check system resources
   top
   df -h
   
   # Optimize database
   sqlite3 src/craft_ai.db "VACUUM;"
   ```

2. **Memory Usage**
   ```bash
   # Monitor memory
   free -h
   
   # Restart application if needed
   sudo systemctl restart craft-ai-dashboard
   ```

## 📞 Support & Maintenance

### **Getting Help**

1. **Check Documentation**
   - README.md for feature overview
   - API documentation for integration
   - User guide for functionality

2. **Log Analysis**
   ```bash
   # View recent logs
   tail -100 app.log
   
   # Search for errors
   grep -i error app.log
   ```

3. **System Status**
   ```bash
   # Check service status
   sudo systemctl status craft-ai-dashboard
   
   # Check network connectivity
   curl -I http://localhost:5000
   ```

### **Maintenance Schedule**

- **Daily**: Monitor logs and performance
- **Weekly**: Check for security updates
- **Monthly**: Database backup and cleanup
- **Quarterly**: Full system review and updates

## 🎯 Success Criteria

After successful deployment, verify:

- ✅ **Login Works**: Demo credentials authenticate successfully
- ✅ **Dashboard Loads**: All metrics and charts display correctly
- ✅ **Navigation Works**: All modules accessible via sidebar
- ✅ **Header Panels**: Visible on all modules with search functionality
- ✅ **Outbound Calls**: Call type filtering dropdown works
- ✅ **Data Filtering**: All filter combinations work correctly
- ✅ **Responsive Design**: Works on desktop and mobile
- ✅ **Performance**: Pages load within 2-3 seconds

## 📋 Deployment Checklist

### **Pre-Deployment**
- [ ] Review system requirements
- [ ] Prepare deployment environment
- [ ] Configure security settings
- [ ] Set up monitoring

### **Deployment**
- [ ] Upload/deploy application
- [ ] Verify database initialization
- [ ] Test authentication
- [ ] Check all modules

### **Post-Deployment**
- [ ] Verify all features work
- [ ] Test call type filtering
- [ ] Check header panels
- [ ] Monitor performance
- [ ] Document deployment details

---

**Craft AI Dashboard v2.2.0 Deployment Guide** - Complete deployment instructions for the enhanced multi-clinic management platform.

