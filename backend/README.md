# Craft AI Dashboard - Multi-Clinic Management Platform

A comprehensive dashboard system for AI-powered clinic management with WhatsApp integration, call tracking, and multi-platform messaging support.

## 🚀 Latest Updates (Fixed Version)

### ✅ **Login Input Field Issue - RESOLVED**
- **Fixed**: Clinic name and username input fields are now fully clickable and functional
- **Issue**: CSS z-index and pointer-events problem was preventing user interaction
- **Solution**: Enhanced CSS with proper layering and pointer-events management

### 🔧 **Technical Improvements**
- Enhanced login page CSS with proper z-index management
- Fixed background overlay interference with input fields
- Improved cross-browser compatibility
- Optimized UI responsiveness

## 📋 Features

### 🏥 **Multi-Clinic Support**
- Clinic-specific user management
- Role-based access control (Super Admin, Clinic Admin)
- Centralized dashboard with clinic-specific data

### 📞 **Communication Management**
- **WhatsApp Integration**: Send/receive messages, view conversations
- **SMS Inbox**: Handle SMS communications with response capabilities
- **Telegram Support**: Manage Telegram conversations
- **Call Data Tracking**: Monitor call volumes and performance metrics

### 📊 **Analytics & Reporting**
- Real-time dashboard with key metrics
- Call volume analysis with hourly breakdowns
- Message distribution analytics
- Performance tracking with "vs yesterday" comparisons

### 📅 **Appointment Management**
- Appointment scheduling and tracking
- Status management (Confirmed, Pending, Cancelled, Completed)
- Calendar integration

### ⚙️ **System Management**
- Outbound call management
- WhatsApp configuration
- System health monitoring
- User activity tracking

## 🔐 Authentication

### Default Credentials
- **Super Admin**: `craft_admin` / `CraftAI2024!`
- **Demo User**: `demo` / `demo` (works with any clinic name)

### Security Features
- JWT-based authentication
- Role-based access control
- Secure session management
- Password encryption

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite (configurable for PostgreSQL/MySQL)
- **Authentication**: Flask-JWT-Extended
- **Real-time**: Flask-SocketIO
- **CORS**: Flask-CORS for cross-origin requests

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **UI Components**: Shadcn/UI
- **Icons**: Lucide React
- **Charts**: Recharts
- **Build Tool**: Vite

## 📦 Quick Start

### Option 1: Docker Deployment (Recommended)
```bash
# Clone/extract the deployment package
cd craft-ai-dashboard-fixed-deployment

# Build and run with Docker Compose
docker-compose up --build -d

# Access the application
open http://localhost:5000
```

### Option 2: Manual Setup
```bash
# Backend setup
cd craft-ai-dashboard-fixed-deployment
pip install -r requirements.txt
python app.py

# Frontend development (optional)
cd frontend_src
npm install
npm run dev
```

### Option 3: Production Deployment
See `deployment-guide.md` for detailed production deployment instructions.

## 🌐 Live Demo

The application is currently deployed at:
**https://60h5imcyqzzl.manus.space**

## 📁 Project Structure

```
craft-ai-dashboard-fixed-deployment/
├── app.py                 # Flask application entry point
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Multi-service deployment
├── src/                  # Backend source code
│   ├── main.py          # Flask app configuration
│   ├── config.py        # Application configuration
│   ├── routes/          # API routes
│   ├── models/          # Database models
│   └── static/          # Built frontend files
├── frontend_src/         # Frontend source code
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── lib/         # Utilities and services
│   │   └── assets/      # Static assets
│   ├── package.json     # Node.js dependencies
│   └── vite.config.js   # Build configuration
├── docs/                 # Documentation
│   ├── deployment-guide.md
│   ├── api-documentation.md
│   └── user-guide.md
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:

```env
# Database
DATABASE_URL=sqlite:///craft_ai.db

# JWT Secret
JWT_SECRET_KEY=your-secret-key-here

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False

# CORS Settings
CORS_ORIGINS=*
```

### Database Setup
The application automatically creates the database and default admin user on first run.

## 📚 Documentation

- **[Deployment Guide](docs/deployment-guide.md)**: Comprehensive deployment instructions
- **[API Documentation](docs/api-documentation.md)**: REST API reference
- **[User Guide](docs/user-guide.md)**: End-user documentation

## 🐛 Troubleshooting

### Common Issues

1. **Login fields not clickable**: This issue has been fixed in this version
2. **CORS errors**: Ensure CORS is properly configured in the backend
3. **Database connection**: Check DATABASE_URL in environment variables
4. **Port conflicts**: Default port is 5000, change if needed

### Support
For technical support or questions, please refer to the documentation or create an issue.

## 📄 License

This project is proprietary software. All rights reserved.

## 🤝 Contributing

This is a private project. For authorized contributors, please follow the development guidelines in the documentation.

---

**Version**: 2.1.0 (Fixed Login Issue)  
**Last Updated**: January 2025  
**Status**: Production Ready ✅

