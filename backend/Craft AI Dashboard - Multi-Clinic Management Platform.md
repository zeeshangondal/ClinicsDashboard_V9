# Craft AI Dashboard - Multi-Clinic Management Platform

**Version**: 2.1.0 (Login Fix Update)  
**Live Application**: https://y0h0i3cqj1eo.manus.space  
**Last Updated**: July 23, 2025

## 🎉 Latest Updates

### Version 2.1.0 - Login Fix Update
- ✅ **FIXED**: Login functionality now works perfectly
- ✅ **FIXED**: Automatic demo account creation on deployment
- ✅ **IMPROVED**: Database initialization with proper seeding
- ✅ **ENHANCED**: Refined header design with neutral colors
- ✅ **ADDED**: End Handoff functionality for WhatsApp, SMS, and Telegram
- ✅ **UPDATED**: Login page design with icons and sleek styling

## 🚀 Quick Start

### Demo Login Credentials
```
Demo User:
  Clinic Name: Demo Clinic
  Username: demo
  Password: demo

Super Admin:
  Username: craft_admin
  Password: CraftAI2024!
```

### Live Application
Access the fully functional application at: **https://y0h0i3cqj1eo.manus.space**

## 📋 Features

### Core Functionality
- **Multi-Clinic Management**: Support for multiple clinic accounts
- **User Authentication**: Secure login with JWT tokens
- **Role-Based Access**: Admin and Super Admin roles
- **Real-Time Dashboard**: Live metrics and system status
- **Communication Modules**: WhatsApp, SMS, and Telegram integration
- **Handoff System**: Human-to-AI conversation handoff workflow

### Recent Enhancements
- **Automatic Account Creation**: Demo accounts created automatically on deployment
- **Refined UI**: Modern header design with neutral color scheme
- **Input Field Icons**: Beautiful login form with Building2, User, and Lock icons
- **End Handoff Buttons**: Complete workflow for human agent handoff completion
- **Responsive Design**: Works perfectly on desktop and mobile devices

## 🛠 Technical Stack

### Backend
- **Framework**: Flask 2.3+
- **Database**: SQLAlchemy with SQLite/PostgreSQL
- **Authentication**: JWT tokens with Flask-JWT-Extended
- **Real-time**: WebSocket support with Flask-SocketIO
- **API**: RESTful API with CORS support

### Frontend
- **Framework**: React 18+ with modern hooks
- **Styling**: Tailwind CSS with shadcn/ui components
- **Icons**: Lucide React icons
- **Charts**: Recharts for data visualization
- **State Management**: React Context and hooks

### Deployment
- **Platform**: Manus deployment platform
- **Database**: Automatic initialization with demo data
- **CORS**: Configured for cross-origin requests
- **SSL**: HTTPS enabled by default

## 📁 Project Structure

```
craft-ai-dashboard/
├── src/
│   ├── main.py              # Flask application entry point
│   ├── config.py            # Configuration settings
│   ├── models/              # Database models
│   │   ├── user.py          # User model with authentication
│   │   ├── clinic.py        # Clinic management model
│   │   └── ...              # Other models
│   ├── routes/              # API route blueprints
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── admin.py         # Admin management endpoints
│   │   └── ...              # Other route modules
│   └── static/              # Frontend build files
├── app.py                   # Application runner
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── docs/                   # Documentation
    ├── deployment-guide.md  # Detailed deployment instructions
    ├── api-documentation.md # API reference
    └── user-guide.md       # End-user documentation
```

## 🔧 Installation & Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd craft-ai-dashboard
   ```

2. **Backend Setup**
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
   The backend will start on `http://localhost:5000`

3. **Frontend Development** (if modifying frontend)
   ```bash
   cd frontend
   npm install
   npm start
   ```
   Frontend development server runs on `http://localhost:3000`

### Database Initialization
The application automatically creates:
- Database tables on first run
- Super admin account (`craft_admin` / `CraftAI2024!`)
- Demo clinic and user (`Demo Clinic` / `demo` / `demo`)

## 🚀 Deployment Options

### Option 1: Manus Platform (Recommended)
```bash
# Deploy backend with automatic frontend serving
manus deploy backend --framework flask --project-dir .
```

### Option 2: Docker Deployment
```bash
docker-compose up --build -d
```

### Option 3: Manual Deployment
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables (see `.env.example`)
3. Run: `python app.py`

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt password hashing
- **Account Locking**: Automatic account lockout after failed attempts
- **CORS Protection**: Configured cross-origin request handling
- **Input Validation**: Comprehensive input sanitization
- **Audit Logging**: Complete action logging for security

## 📊 Multi-Tenancy Support

Each clinic operates independently with:
- Separate user accounts and data
- Individual subscription management
- Isolated conversation histories
- Custom clinic settings and branding
- Independent billing and usage tracking

## 🤝 Human-AI Handoff Workflow

The platform includes a complete handoff system:
1. **AI Handling**: AI manages conversations initially
2. **Human Escalation**: Complex cases escalated to human agents
3. **Handoff Completion**: Human agents mark conversations as complete
4. **AI Resumption**: AI takes over resolved conversations

## 📞 Communication Channels

### WhatsApp Integration
- Real-time message handling
- Media file support
- Conversation threading
- Status tracking

### SMS Management
- Inbound/outbound SMS
- Bulk messaging capabilities
- Delivery status tracking
- Template management

### Telegram Support
- Bot integration
- Group chat management
- File sharing
- Inline keyboards

## 📈 Analytics & Reporting

- **Real-time Metrics**: Live dashboard with key performance indicators
- **Call Analytics**: Detailed call volume and duration tracking
- **Message Statistics**: Comprehensive messaging analytics
- **Appointment Tracking**: Appointment booking and completion rates
- **System Health**: Server performance and uptime monitoring

## 🔧 Configuration

### Environment Variables
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///craft_ai.db
JWT_SECRET_KEY=your-jwt-secret
CORS_ORIGINS=*
```

### Database Configuration
- **Development**: SQLite (default)
- **Production**: PostgreSQL recommended
- **Automatic Migration**: Flask-Migrate for schema updates

## 📚 API Documentation

The application provides a comprehensive REST API:
- **Authentication**: `/api/auth/*`
- **Admin Management**: `/api/admin/*`
- **Clinic Operations**: `/api/clinics/*`
- **Communication**: `/api/whatsapp/*`, `/api/sms/*`, `/api/telegram/*`

Full API documentation available at `/docs/api-documentation.md`

## 🐛 Troubleshooting

### Common Issues

**Login Failed Error**
- ✅ **RESOLVED**: This issue has been fixed in version 2.1.0
- Demo accounts are now created automatically on deployment

**Database Connection Issues**
- Check database URL configuration
- Ensure database server is running
- Verify connection permissions

**CORS Errors**
- Confirm CORS_ORIGINS environment variable
- Check frontend URL configuration
- Verify API endpoint URLs

## 📞 Support

For technical support or questions:
- Check the documentation in `/docs/`
- Review the troubleshooting section above
- Contact the development team

## 📄 License

This project is proprietary software developed for Craft AI.

---

**🎯 Ready to Use**: The application is fully functional and ready for production use with automatic demo account creation and a complete multi-clinic management system.

