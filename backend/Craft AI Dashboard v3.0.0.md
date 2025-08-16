# Craft AI Dashboard v3.0.0

**Multi-Clinic Management Platform with Enhanced Call Data Analytics**

![Craft AI Logo](https://private-us-east-1.manuscdn.com/sessionFile/9StIISS45yQanQlY0Zb5If/sandbox/9qo5afi7YGDgW3k1ObVMcH-images_1753312377310_na1fn_L2hvbWUvdWJ1bnR1L2NyYWZ0LWFpLWRhc2hib2FyZC12My4wLWZpbmFsLWRlcGxveW1lbnQvc3JjL3N0YXRpYy9hc3NldHMvY3JhZnQtYWktbG9nby1EQUJaam1sLQ.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvOVN0SUlTUzQ1eVFhblFsWTBaYjVJZi9zYW5kYm94LzlxbzVhZmk3WUdEZ1czazFPYlZNY0gtaW1hZ2VzXzE3NTMzMTIzNzczMTBfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyTnlZV1owTFdGcExXUmhjMmhpYjJGeVpDMTJNeTR3TFdacGJtRnNMV1JsY0d4dmVXMWxiblF2YzNKakwzTjBZWFJwWXk5aGMzTmxkSE12WTNKaFpuUXRZV2t0Ykc5bmJ5MUVRVUphYW0xc0xRLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=bunrXKKukuyPqC2GdjeW1WdE35OUT051Pdpe-KZbHroLMaeWMJoGb94XSgM4HyRrz2HBHwe5fIkn6fuT0OV3MwrjhU~FqRGgbAFdG7bXbiUISIOgtbv45KlQWJ7JRZT3VfKRH9yZsgCZkMXno6cT0mpv0ZsQeSKsb6sLLPXh-uYLOgz8RP40utcEjNcwkFlU7fjpRjGU2LBPfcAZF8cqYsT8SeVRnSD1kPbUYDldtslVJJBIoMsZOh4RXROMkMg~UF9FRRyI-qREp4vf4mKNCk1Lg44uDrzA8~bMlF92our8C3Dv9rab2d9cWtUV6KYVA8u7~Efa4uKQ-2j8TTqRbg__)

## 🚀 Live Application

**Production URL**: https://w5hni7c7qomo.manus.space

**Demo Credentials**:
- **Clinic Name**: Demo Clinic
- **Username**: demo
- **Password**: demo

**Super Admin Access**:
- **Username**: craft_admin
- **Password**: CraftAI2024!

## 📋 Version 3.0.0 Features

### ✨ **New in v3.0.0**
- **Enhanced Call Data Analytics**: Call Reason column and filtering system
- **Streamlined Navigation**: Removed Outbound Calls dashboard for simplified workflow
- **Professional Branding**: Updated logo integration throughout the platform
- **Improved User Experience**: Single header panel across all modules

### 🎯 **Core Features**
- **Multi-Clinic Management**: Support for multiple clinic operations
- **Call Data Analytics**: Comprehensive call tracking with reason-based filtering
- **WhatsApp Integration**: Message management and automation
- **SMS Management**: Inbox and outbound messaging
- **Telegram Integration**: Multi-platform communication
- **Appointment Scheduling**: Calendar and booking management
- **Real-time Dashboard**: Live metrics and performance indicators

## 🏗️ **Technical Architecture**

### **Backend Stack**
- **Framework**: Flask (Python)
- **Database**: SQLAlchemy with SQLite/PostgreSQL support
- **Authentication**: JWT-based secure authentication
- **API**: RESTful API with comprehensive endpoints
- **CORS**: Cross-origin resource sharing enabled

### **Frontend Stack**
- **Framework**: React 18 with Vite
- **UI Library**: Tailwind CSS + shadcn/ui components
- **Icons**: Lucide React
- **Charts**: Recharts for data visualization
- **State Management**: React hooks and context

### **Deployment**
- **Platform**: Manus Cloud Platform
- **Environment**: Production-ready with auto-scaling
- **SSL**: HTTPS enabled with automatic certificate management
- **CDN**: Global content delivery network

## 📊 **Call Data Analytics Features**

### **Call Reason Tracking**
The enhanced Call Data section now includes comprehensive call reason tracking:

- **Birthday Call**: Customer birthday greetings and special offers
- **Appointment Confirmation**: Confirming upcoming appointments
- **Booking Call**: New appointment scheduling calls
- **Follow-up Call**: Post-treatment or consultation follow-ups
- **Consultation Call**: Initial consultation and assessment calls
- **Reminder Call**: Appointment and treatment reminders
- **Sales Call**: Service promotion and upselling calls
- **Support Call**: Customer support and issue resolution
- **General Inquiry**: General information requests
- **Billing Inquiry**: Payment and billing related calls

### **Advanced Filtering**
- **Status Filter**: Completed, Missed, In Progress, Failed
- **Direction Filter**: Inbound, Outbound
- **Call Reason Filter**: Filter by specific call purposes
- **Search Function**: Search by contact name or phone number
- **Date Range**: Historical call data analysis

### **Analytics Dashboard**
- **Real-time Metrics**: Live call statistics and performance indicators
- **Trend Analysis**: Call volume trends and success rates
- **Duration Tracking**: Average call duration and efficiency metrics
- **Success Rate**: Call completion and conversion tracking

## 🔧 **Quick Start Guide**

### **1. Access the Application**
Visit https://w5hni7c7qomo.manus.space and log in with the demo credentials.

### **2. Navigate the Dashboard**
- **Dashboard**: Overview of all clinic activities and metrics
- **Call Data**: Detailed call analytics with reason-based filtering
- **WhatsApp**: Message management and automation
- **SMS Inbox**: SMS communication management
- **Telegram**: Multi-platform messaging
- **Appointments**: Calendar and scheduling management

### **3. Use Call Data Analytics**
1. Click on "Call Data" in the sidebar
2. Use the "All Reasons" dropdown to filter calls by purpose
3. Apply additional filters for status and direction
4. Search for specific contacts or phone numbers
5. Export data for external analysis

## 🛠️ **Development Setup**

### **Prerequisites**
- Python 3.11+
- Node.js 20+
- npm or yarn

### **Backend Setup**
```bash
# Clone the repository
git clone <repository-url>
cd craft-ai-dashboard-v3.0-final-deployment

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python -c "from src.main import app, db; app.app_context().push(); db.create_all()"

# Run the application
python app.py
```

### **Frontend Development**
```bash
# Navigate to frontend directory (if developing separately)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## 🚀 **Deployment Options**

### **1. Manus Platform (Recommended)**
The application is optimized for deployment on the Manus platform with automatic scaling and SSL.

### **2. Docker Deployment**
```bash
# Build and run with Docker
docker-compose up -d
```

### **3. Manual Server Deployment**
Detailed instructions available in `docs/deployment-guide.md`

## 📚 **Documentation**

- **Deployment Guide**: `docs/deployment-guide.md`
- **API Documentation**: `docs/api-documentation.md`
- **User Guide**: `docs/user-guide.md`
- **Changelog**: `CHANGELOG.md`

## 🔐 **Security Features**

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt password encryption
- **CORS Protection**: Configured cross-origin resource sharing
- **Input Validation**: Comprehensive input sanitization
- **SQL Injection Prevention**: Parameterized queries with SQLAlchemy

## 📈 **Performance Optimizations**

- **Database Indexing**: Optimized database queries
- **Caching**: Strategic caching for improved response times
- **Code Splitting**: Optimized frontend bundle sizes
- **CDN Integration**: Global content delivery
- **Compression**: Gzip compression for faster loading

## 🆘 **Support & Troubleshooting**

### **Common Issues**
1. **Login Issues**: Ensure correct clinic name, username, and password
2. **Data Not Loading**: Check internet connection and refresh the page
3. **Filter Not Working**: Clear browser cache and try again

### **Contact Support**
- **Email**: support@craftai.com
- **Documentation**: Comprehensive guides in the `docs/` directory
- **Live Application**: https://w5hni7c7qomo.manus.space

## 📄 **License**

This project is proprietary software developed for Craft AI. All rights reserved.

## 🏷️ **Version Information**

- **Version**: 3.0.0
- **Release Date**: January 2024
- **Compatibility**: Modern browsers (Chrome 90+, Firefox 88+, Safari 14+)
- **Mobile Support**: Responsive design for mobile and tablet devices

---

**Craft AI Dashboard v3.0.0** - Empowering clinics with intelligent communication management and analytics.

