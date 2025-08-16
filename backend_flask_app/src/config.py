import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'craft-ai-default-secret-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'craft-ai-jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 900)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 604800)))
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    
    # Use a file-based SQLite database that's writable
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # WhatsApp Business API Configuration
    WHATSAPP_API_VERSION = 'v21.0'
    WHATSAPP_BASE_URL = 'https://graph.facebook.com'
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = '/tmp/uploads'
    
    # Pagination defaults
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/1'

