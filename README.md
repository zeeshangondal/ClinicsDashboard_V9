# Craft AI Dashboard - Deployment Guide

This document provides comprehensive instructions for deploying the Craft AI Dashboard application, which consists of a React frontend and a Flask backend.

## Application Structure

```
craft-ai-dashboard-deployment/
├── app.py                 # Main Flask application entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── src/                   # Backend source code
│   ├── main.py            # Flask application logic
│   ├── config.py          # Configuration settings
│   ├── routes/            # API routes
│   └── static/            # Built frontend files served by Flask
└── craft-ai-dashboard-frontend/  # Frontend source code
    ├── package.json       # Node.js dependencies
    ├── vite.config.js     # Vite configuration
    ├── src/               # React source code
    └── public/            # Public assets
```

## Prerequisites

- Python 3.8+ with pip
- Node.js 16+ with npm
- Git

## Deployment Steps

### 1. Backend Setup

1. Create a virtual environment:
   ```bash
   cd craft-ai-dashboard-deployment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - The `.env` file is already included with default settings
   - Modify as needed for your environment

### 2. Frontend Setup

1. Install dependencies:
   ```bash
   cd craft-ai-dashboard-frontend
   npm install
   ```

2. Build the frontend:
   ```bash
   npm run build
   ```

3. Copy the built files to the backend static directory:
   ```bash
   cp -r dist/* ../src/static/
   ```
   On Windows:
   ```
   xcopy /E /I dist\* ..\src\static\
   ```

### 3. Running the Application

#### Development Mode

1. Start the backend:
   ```bash
   cd craft-ai-dashboard-deployment
   python app.py
   ```

2. In a separate terminal, start the frontend development server:
   ```bash
   cd craft-ai-dashboard-frontend
   npm run dev
   ```

#### Production Mode

1. Build the frontend as described above

2. Start the Flask application:
   ```bash
   cd craft-ai-dashboard-deployment
   python app.py
   ```

3. The application will be available at `http://localhost:5000`

### 4. Deployment to Production Server

#### Option 1: Manual Deployment

1. Set up a production server with Python and required dependencies
2. Clone or copy this repository to the server
3. Follow the steps above to build the frontend and start the application
4. Configure a reverse proxy (Nginx, Apache) to serve the application

#### Option 2: Docker Deployment

A Dockerfile is provided for containerized deployment:

1. Build the Docker image:
   ```bash
   docker build -t craft-ai-dashboard .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 craft-ai-dashboard
   ```

#### Option 3: Cloud Deployment

The application can be deployed to various cloud platforms:

- **Heroku**: Use the provided `Procfile`
- **AWS Elastic Beanstalk**: Use the provided `Dockerfile`
- **Google Cloud Run**: Use the provided `Dockerfile`

## Authentication

The application includes two types of authentication:

1. **Super Admin**:
   - Username: `craft_admin`
   - Password: `CraftAI2024!`

2. **Clinic User**:
   - Username: `demo`
   - Password: `demo`
   - Clinic Name: Any clinic name can be used

## Customization

### Frontend Customization

1. Modify the React components in `craft-ai-dashboard-frontend/src/components/`
2. Update styles in `craft-ai-dashboard-frontend/src/App.css`
3. Rebuild the frontend with `npm run build`
4. Copy the built files to the backend static directory

### Backend Customization

1. Modify API routes in `src/routes/`
2. Update database configuration in `src/config.py`
3. Add new features by extending the Flask application in `src/main.py`

## Troubleshooting

### Common Issues

1. **Frontend not loading**: Ensure the built files are correctly copied to the `src/static` directory
2. **API errors**: Check the Flask logs for backend errors
3. **Database connection issues**: Verify the database configuration in `.env`

### Support

For additional support or questions, please contact the development team.

## License

This application is proprietary software. All rights reserved.

---

© 2024 Craft AI Dashboard

