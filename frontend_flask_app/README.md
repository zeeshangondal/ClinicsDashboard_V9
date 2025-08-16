# Craft AI Dashboard - Multi-Clinic Management Platform

**Version**: 2.2.0 (Outbound Calls Enhancement Update)  
**Live Demo**: https://zmhqivcv1g9m.manus.space  
**Status**: ✅ Fully Functional

## 🎯 Latest Updates (v2.2.0)

### ✨ **New Features**
- **Enhanced Outbound Calls Module**: Added call type filtering similar to Call Data section
- **Universal Header Panels**: Header now appears on all modules, not just the main dashboard
- **Call Type Filtering**: Filter outbound calls by type (birthday calls, appointment confirmations, etc.)
- **Updated Logo**: New Craft AI logo integrated throughout the application

### 🔧 **Improvements**
- Fixed login authentication and dashboard display issues
- Enhanced user interface consistency across all modules
- Improved navigation and user experience
- Better data organization and filtering capabilities

## 🚀 Quick Start

### **Demo Access**
- **URL**: https://zmhqivcv1g9m.manus.space
- **Clinic Name**: Demo Clinic
- **Username**: demo
- **Password**: demo

### **Super Admin Access**
- **Username**: craft_admin
- **Password**: CraftAI2024!

## 📋 Features Overview

### **Core Modules**
- ✅ **Dashboard**: Comprehensive overview with metrics and charts
- ✅ **Call Data**: Advanced call analytics with filtering
- ✅ **Outbound Calls**: Lead management with call type filtering *(NEW)*
- ✅ **WhatsApp Integration**: Message management and automation
- ✅ **SMS Inbox**: Centralized SMS communication
- ✅ **Telegram**: Multi-platform messaging support
- ✅ **Appointments**: Scheduling and calendar management
- ✅ **WhatsApp Config**: Configuration and settings

### **Enhanced Outbound Calls Features** *(NEW)*
- **Call Type Filtering**: Filter by birthday calls, appointment confirmations, follow-ups, etc.
- **Lead Management**: Comprehensive lead tracking and management
- **Campaign Management**: Organize and track calling campaigns
- **Priority Filtering**: Filter leads by priority level
- **Status Tracking**: Monitor call status and outcomes
- **Search Functionality**: Search by name, phone, or email

### **Universal Enhancements** *(NEW)*
- **Header Panels**: Consistent header across all modules with search and user info
- **Improved Navigation**: Better user experience across the platform
- **Enhanced UI**: Updated logo and visual consistency

## 🛠 Technical Stack

### **Backend**
- **Framework**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT-based authentication
- **API**: RESTful API design

### **Frontend**
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Charts**: Recharts
- **State Management**: React Hooks

### **Infrastructure**
- **Deployment**: Manus Platform
- **Static Files**: Integrated with Flask backend
- **CORS**: Configured for cross-origin requests

## 📁 Project Structure

```
craft-ai-dashboard-v2.2-final-deployment/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── src/
│   ├── main.py           # Application initialization
│   ├── models/           # Database models
│   │   ├── user.py
│   │   ├── clinic.py
│   │   └── call.py       # Call model with types
│   ├── routes/           # API routes
│   │   ├── auth.py
│   │   ├── admin.py
│   │   └── calls.py      # Call filtering API (NEW)
│   ├── decorators.py     # Authentication decorators
│   ├── seed_data.py      # Demo data generation (NEW)
│   └── static/           # Built frontend files
└── docs/                 # Documentation
    ├── deployment-guide.md
    ├── api-documentation.md
    └── user-guide.md
```

## 🔧 Installation & Deployment

### **Option 1: Manus Platform (Recommended)**
1. Upload the deployment package to Manus
2. Deploy using the Flask framework option
3. Access your deployed application URL

### **Option 2: Local Development**
```bash
# Clone or extract the deployment package
cd craft-ai-dashboard-v2.2-final-deployment

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Access at http://localhost:5000
```

### **Option 3: Docker**
```bash
# Build and run with Docker
docker build -t craft-ai-dashboard .
docker run -p 5000:5000 craft-ai-dashboard
```

## 🔐 Authentication

### **Demo Account**
- **Purpose**: Testing and demonstration
- **Clinic**: Demo Clinic
- **Credentials**: demo / demo
- **Permissions**: Full clinic access

### **Super Admin Account**
- **Purpose**: System administration
- **Credentials**: craft_admin / CraftAI2024!
- **Permissions**: Cross-clinic access and management

## 📊 Call Type Filtering *(NEW FEATURE)*

The enhanced Outbound Calls module now supports filtering by call types:

### **Available Call Types**
- **Birthday Call**: Customer birthday greetings
- **Appointment Confirmation**: Confirming upcoming appointments
- **Follow-up Call**: Post-service follow-ups
- **Consultation Call**: Initial consultations
- **Reminder Call**: General reminders
- **Sales Call**: Sales and promotional calls
- **Support Call**: Customer support calls

### **How to Use**
1. Navigate to **Outbound Calls** → **Individual Leads**
2. Use the **"All Call Types"** dropdown to filter
3. Combine with other filters (status, priority, search)
4. View filtered results in real-time

## 🎨 UI/UX Enhancements

### **New Logo Integration**
- Updated Craft AI logo throughout the application
- Consistent branding across all modules
- Professional visual identity

### **Universal Header Panels**
- Header now appears on all modules
- Consistent search functionality
- User profile and settings access
- Improved navigation experience

## 📈 Performance & Scalability

- **Optimized Database Queries**: Efficient filtering and pagination
- **Responsive Design**: Works on desktop and mobile devices
- **Fast Loading**: Optimized frontend build with Vite
- **Scalable Architecture**: Modular design for easy expansion

## 🔍 API Endpoints *(NEW)*

### **Call Type Filtering**
```
GET /api/calls/types
- Returns available call types

GET /api/calls/outbound?call_type=birthday_call
- Filter outbound calls by type

GET /api/calls/outbound?status=interested&priority=high&call_type=consultation
- Combined filtering support
```

## 🐛 Troubleshooting

### **Common Issues**
1. **Login Issues**: Ensure correct clinic name and credentials
2. **Data Not Loading**: Check browser console for errors
3. **Filtering Not Working**: Verify API endpoints are accessible

### **Support**
- Check the deployment guide for detailed instructions
- Review the API documentation for integration details
- Contact support for technical assistance

## 📝 Changelog

### **Version 2.2.0** *(Current)*
- ✅ Added call type filtering to Outbound Calls module
- ✅ Implemented universal header panels across all modules
- ✅ Integrated new Craft AI logo
- ✅ Fixed login authentication issues
- ✅ Enhanced user interface consistency
- ✅ Added comprehensive call type management

### **Version 2.1.0**
- ✅ Fixed login functionality
- ✅ Added automatic demo account creation
- ✅ Improved database initialization

### **Version 2.0.0**
- ✅ Initial multi-clinic dashboard implementation
- ✅ Core modules and functionality

## 📄 License

This project is proprietary software developed for Craft AI. All rights reserved.

---

**Craft AI Dashboard v2.2.0** - Empowering clinics with intelligent communication management.

