from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    clinic_id = Column(String(36), ForeignKey('clinics.id', ondelete='CASCADE'))
    username = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(String(50), nullable=False, default='agent')
    permissions = Column(JSON, default=[])
    is_active = Column(Boolean, nullable=False, default=True)
    last_login_at = Column(DateTime)
    password_changed_at = Column(DateTime, default=datetime.utcnow)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    clinic = relationship("Clinic", back_populates="users")
    assigned_leads = relationship("Lead", back_populates="assigned_user")
    assigned_conversations = relationship("WhatsAppConversation", back_populates="assigned_agent")
    created_appointments = relationship("Appointment", back_populates="created_by_user")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    def __init__(self, **kwargs):
        if 'password' in kwargs:
            self.set_password(kwargs.pop('password'))
        super(User, self).__init__(**kwargs)
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)
        self.password_changed_at = datetime.utcnow()
    
    def check_password(self, password):
        """Check if the provided password matches the user's password"""
        return check_password_hash(self.password_hash, password)
    
    def is_locked(self):
        """Check if the user account is locked"""
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False
    
    def increment_failed_login(self):
        """Increment failed login attempts and lock account if necessary"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.locked_until = datetime.utcnow() + timedelta(minutes=30)
        db.session.commit()
    
    def reset_failed_login(self):
        """Reset failed login attempts after successful login"""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.last_login_at = datetime.utcnow()
        db.session.commit()
    
    def has_permission(self, permission):
        """Check if user has a specific permission"""
        if self.role == 'super_admin':
            return True
        return permission in (self.permissions or [])
    
    def has_role(self, role):
        """Check if user has a specific role"""
        return self.role == role
    
    def can_access_clinic(self, clinic_id):
        """Check if user can access a specific clinic"""
        if self.role == 'super_admin':
            return True
        return str(self.clinic_id) == str(clinic_id)
    
    def to_dict(self, include_sensitive=False):
        data = {
            'id': self.id,
            'clinic_id': self.clinic_id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'permissions': self.permissions,
            'is_active': self.is_active,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_locked': self.is_locked()
        }
        
        if include_sensitive:
            data.update({
                'failed_login_attempts': self.failed_login_attempts,
                'locked_until': self.locked_until.isoformat() if self.locked_until else None,
                'password_changed_at': self.password_changed_at.isoformat() if self.password_changed_at else None
            })
        
        return data
    
    @classmethod
    def create_user(cls, clinic_id, username, email, password, role='agent', **kwargs):
        """Create a new user with hashed password"""
        # Check for unique username within clinic
        existing_user = cls.query.filter_by(clinic_id=clinic_id, username=username).first()
        if existing_user:
            raise ValueError("Username already exists in this clinic")
        
        # Check for unique email within clinic
        existing_email = cls.query.filter_by(clinic_id=clinic_id, email=email).first()
        if existing_email:
            raise ValueError("Email already exists in this clinic")
        
        user = cls(
            clinic_id=clinic_id,
            username=username,
            email=email,
            password=password,
            role=role,
            **kwargs
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    @classmethod
    def create_super_admin(cls, username, email, password, **kwargs):
        """Create a super admin user (not associated with any clinic)"""
        existing_user = cls.query.filter_by(username=username, role='super_admin').first()
        if existing_user:
            raise ValueError("Super admin username already exists")
        
        user = cls(
            clinic_id=None,
            username=username,
            email=email,
            password=password,
            role='super_admin',
            **kwargs
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'

# Import to avoid circular imports
from datetime import timedelta
