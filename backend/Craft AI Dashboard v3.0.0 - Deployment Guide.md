# Craft AI Dashboard v3.0.0 - Deployment Guide

This comprehensive guide covers all deployment options for the Craft AI Dashboard, from quick cloud deployment to enterprise-grade server installations.

## 🚀 Quick Deployment (Recommended)

### Manus Platform Deployment

The fastest way to deploy Craft AI Dashboard is using the Manus platform, which provides automatic scaling, SSL certificates, and global CDN.

#### Prerequisites
- Manus account (sign up at https://manus.space)
- Project files (this deployment package)

#### Deployment Steps

1. **Prepare the Project**
   ```bash
   # Ensure all files are in the project directory
   cd craft-ai-dashboard-v3.0-final-deployment
   
   # Verify required files exist
   ls -la app.py requirements.txt src/
   ```

2. **Deploy to Manus**
   ```bash
   # Using Manus CLI (if available)
   manus deploy --framework flask --project-dir .
   
   # Or upload via web interface
   # Zip the project and upload to Manus dashboard
   ```

3. **Configure Environment Variables**
   Set the following environment variables in the Manus dashboard:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///app.db
   JWT_SECRET_KEY=your-jwt-secret-here
   ```

4. **Access Your Application**
   Your application will be available at a URL like: `https://your-app-id.manus.space`

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   
   services:
     web:
       build: .
       ports:
         - "5000:5000"
       environment:
         - FLASK_ENV=production
         - SECRET_KEY=your-secret-key-here
         - DATABASE_URL=sqlite:///app.db
         - JWT_SECRET_KEY=your-jwt-secret-here
       volumes:
         - ./data:/app/data
       restart: unless-stopped
   
     nginx:
       image: nginx:alpine
       ports:
         - "80:80"
         - "443:443"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf
         - ./ssl:/etc/nginx/ssl
       depends_on:
         - web
       restart: unless-stopped
   ```

2. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       gcc \
       && rm -rf /var/lib/apt/lists/*
   
   # Copy requirements and install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   # Copy application code
   COPY . .
   
   # Create data directory
   RUN mkdir -p data
   
   # Expose port
   EXPOSE 5000
   
   # Run the application
   CMD ["python", "app.py"]
   ```

3. **Deploy with Docker Compose**
   ```bash
   # Build and start services
   docker-compose up -d
   
   # View logs
   docker-compose logs -f
   
   # Stop services
   docker-compose down
   ```

### Using Docker Only

```bash
# Build the image
docker build -t craft-ai-dashboard .

# Run the container
docker run -d \
  --name craft-ai-dashboard \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key-here \
  -v $(pwd)/data:/app/data \
  craft-ai-dashboard
```

## 🖥️ Manual Server Deployment

### Ubuntu/Debian Server

#### 1. System Preparation

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and required packages
sudo apt install -y python3 python3-pip python3-venv nginx supervisor

# Install Node.js (for frontend development)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### 2. Application Setup

```bash
# Create application directory
sudo mkdir -p /var/www/craft-ai-dashboard
cd /var/www/craft-ai-dashboard

# Copy application files
sudo cp -r /path/to/craft-ai-dashboard-v3.0-final-deployment/* .

# Set ownership
sudo chown -R www-data:www-data /var/www/craft-ai-dashboard

# Create virtual environment
sudo -u www-data python3 -m venv venv
sudo -u www-data venv/bin/pip install -r requirements.txt
```

#### 3. Database Setup

```bash
# Initialize database
sudo -u www-data venv/bin/python -c "
from src.main import app, db
with app.app_context():
    db.create_all()
    print('Database initialized successfully')
"
```

#### 4. Supervisor Configuration

Create `/etc/supervisor/conf.d/craft-ai-dashboard.conf`:

```ini
[program:craft-ai-dashboard]
command=/var/www/craft-ai-dashboard/venv/bin/python app.py
directory=/var/www/craft-ai-dashboard
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/craft-ai-dashboard.log
environment=FLASK_ENV=production,SECRET_KEY=your-secret-key-here,DATABASE_URL=sqlite:///app.db,JWT_SECRET_KEY=your-jwt-secret-here
```

```bash
# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start craft-ai-dashboard
```

#### 5. Nginx Configuration

Create `/etc/nginx/sites-available/craft-ai-dashboard`:

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
    
    location /static {
        alias /var/www/craft-ai-dashboard/src/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/craft-ai-dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 6. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### CentOS/RHEL Server

#### 1. System Preparation

```bash
# Update system
sudo yum update -y

# Install EPEL repository
sudo yum install -y epel-release

# Install Python and required packages
sudo yum install -y python3 python3-pip nginx supervisor

# Install Node.js
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo yum install -y nodejs
```

#### 2. Follow similar steps as Ubuntu

The application setup, database initialization, and configuration steps are similar to Ubuntu. Adjust package manager commands and file paths as needed for CentOS/RHEL.

## ☁️ Cloud Platform Deployment

### AWS Deployment

#### Using AWS Elastic Beanstalk

1. **Prepare Application**
   ```bash
   # Create .ebextensions directory
   mkdir .ebextensions
   
   # Create configuration file
   cat > .ebextensions/python.config << EOF
   option_settings:
     aws:elasticbeanstalk:container:python:
       WSGIPath: app.py
     aws:elasticbeanstalk:application:environment:
       FLASK_ENV: production
       SECRET_KEY: your-secret-key-here
       DATABASE_URL: sqlite:///app.db
       JWT_SECRET_KEY: your-jwt-secret-here
   EOF
   ```

2. **Deploy with EB CLI**
   ```bash
   # Install EB CLI
   pip install awsebcli
   
   # Initialize and deploy
   eb init craft-ai-dashboard
   eb create production
   eb deploy
   ```

#### Using AWS EC2

1. **Launch EC2 Instance**
   - Choose Ubuntu 22.04 LTS AMI
   - Select appropriate instance type (t3.medium recommended)
   - Configure security groups (ports 22, 80, 443)

2. **Follow Manual Server Deployment Steps**
   Use the Ubuntu server deployment instructions above.

### Google Cloud Platform

#### Using Google App Engine

1. **Create app.yaml**
   ```yaml
   runtime: python311
   
   env_variables:
     FLASK_ENV: production
     SECRET_KEY: your-secret-key-here
     DATABASE_URL: sqlite:///app.db
     JWT_SECRET_KEY: your-jwt-secret-here
   
   handlers:
   - url: /static
     static_dir: src/static
   
   - url: /.*
     script: auto
   ```

2. **Deploy**
   ```bash
   # Install Google Cloud SDK
   # Follow: https://cloud.google.com/sdk/docs/install
   
   # Deploy application
   gcloud app deploy
   ```

### Microsoft Azure

#### Using Azure App Service

1. **Create Web App**
   ```bash
   # Install Azure CLI
   # Follow: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
   
   # Create resource group
   az group create --name craft-ai-rg --location "East US"
   
   # Create App Service plan
   az appservice plan create --name craft-ai-plan --resource-group craft-ai-rg --sku B1 --is-linux
   
   # Create web app
   az webapp create --resource-group craft-ai-rg --plan craft-ai-plan --name craft-ai-dashboard --runtime "PYTHON|3.11"
   ```

2. **Deploy Code**
   ```bash
   # Deploy from local Git
   az webapp deployment source config-local-git --name craft-ai-dashboard --resource-group craft-ai-rg
   
   # Add Azure remote and push
   git remote add azure <deployment-url>
   git push azure main
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False

# Database Configuration
DATABASE_URL=sqlite:///app.db
# For PostgreSQL: postgresql://username:password@localhost/dbname
# For MySQL: mysql://username:password@localhost/dbname

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600

# Application Configuration
APP_NAME=Craft AI Dashboard
APP_VERSION=3.0.0

# CORS Configuration
CORS_ORIGINS=*

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=app.log

# Email Configuration (if needed)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# External API Keys (if needed)
OPENAI_API_KEY=your-openai-api-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
```

### Database Configuration

#### SQLite (Default)
```python
DATABASE_URL=sqlite:///app.db
```

#### PostgreSQL
```python
DATABASE_URL=postgresql://username:password@localhost:5432/craft_ai_db
```

#### MySQL
```python
DATABASE_URL=mysql://username:password@localhost:3306/craft_ai_db
```

### Security Configuration

#### SSL/TLS Setup

1. **Obtain SSL Certificate**
   - Use Let's Encrypt for free certificates
   - Purchase from a certificate authority
   - Use cloud provider's certificate service

2. **Configure Nginx for SSL**
   ```nginx
   server {
       listen 443 ssl http2;
       server_name your-domain.com;
       
       ssl_certificate /path/to/certificate.crt;
       ssl_certificate_key /path/to/private.key;
       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   
   server {
       listen 80;
       server_name your-domain.com;
       return 301 https://$server_name$request_uri;
   }
   ```

## 📊 Monitoring and Maintenance

### Health Checks

Create a health check endpoint:

```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

### Logging Configuration

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Backup Strategy

#### Database Backup
```bash
# SQLite backup
cp app.db backup/app_$(date +%Y%m%d_%H%M%S).db

# PostgreSQL backup
pg_dump craft_ai_db > backup/craft_ai_$(date +%Y%m%d_%H%M%S).sql

# Automated backup script
#!/bin/bash
BACKUP_DIR="/var/backups/craft-ai"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
cp /var/www/craft-ai-dashboard/app.db $BACKUP_DIR/app_$DATE.db
find $BACKUP_DIR -name "app_*.db" -mtime +7 -delete
```

#### Application Backup
```bash
# Create application backup
tar -czf backup/craft-ai-app_$(date +%Y%m%d_%H%M%S).tar.gz \
  --exclude='venv' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  /var/www/craft-ai-dashboard
```

### Performance Monitoring

#### System Monitoring
```bash
# Install monitoring tools
sudo apt install -y htop iotop nethogs

# Monitor application processes
ps aux | grep python
netstat -tlnp | grep :5000
```

#### Application Monitoring
```python
# Add performance monitoring
from flask import request
import time

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    app.logger.info(f'{request.method} {request.path} - {response.status_code} - {duration:.3f}s')
    return response
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Application Won't Start
```bash
# Check logs
sudo journalctl -u craft-ai-dashboard -f
tail -f /var/log/craft-ai-dashboard.log

# Check Python environment
source venv/bin/activate
python -c "import flask; print(flask.__version__)"
```

#### 2. Database Connection Issues
```bash
# Check database file permissions
ls -la app.db

# Test database connection
python -c "
from src.main import app, db
with app.app_context():
    try:
        db.engine.execute('SELECT 1')
        print('Database connection successful')
    except Exception as e:
        print(f'Database error: {e}')
"
```

#### 3. Static Files Not Loading
```bash
# Check Nginx configuration
sudo nginx -t

# Check static file permissions
ls -la src/static/

# Test static file serving
curl -I http://your-domain.com/static/css/style.css
```

#### 4. SSL Certificate Issues
```bash
# Check certificate validity
openssl x509 -in /path/to/certificate.crt -text -noout

# Test SSL configuration
openssl s_client -connect your-domain.com:443

# Renew Let's Encrypt certificate
sudo certbot renew --dry-run
```

### Performance Issues

#### 1. Slow Response Times
- Check database query performance
- Enable database query logging
- Implement caching (Redis/Memcached)
- Optimize static file serving

#### 2. High Memory Usage
- Monitor Python memory usage
- Check for memory leaks
- Implement connection pooling
- Optimize database queries

#### 3. High CPU Usage
- Profile application code
- Optimize expensive operations
- Implement background task processing
- Scale horizontally

### Security Issues

#### 1. Authentication Problems
- Check JWT token expiration
- Verify secret key configuration
- Review CORS settings
- Check user permissions

#### 2. HTTPS Issues
- Verify SSL certificate installation
- Check certificate chain
- Review security headers
- Test with SSL Labs

## 📞 Support

For deployment assistance or technical support:

- **Documentation**: Check the complete documentation in the `docs/` directory
- **Live Application**: https://w5hni7c7qomo.manus.space
- **Email Support**: support@craftai.com

---

This deployment guide covers all major deployment scenarios. Choose the method that best fits your infrastructure and requirements.

