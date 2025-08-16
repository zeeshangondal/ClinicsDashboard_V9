from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from src.models.user import db

class Clinic(db.Model):
    __tablename__ = 'clinics'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True)
    subscription_status = Column(String(50), nullable=False, default='trial')
    subscription_plan = Column(String(50), nullable=False, default='basic')
    subscription_expires_at = Column(DateTime)
    max_users = Column(Integer, nullable=False, default=5)
    max_monthly_calls = Column(Integer, nullable=False, default=1000)
    max_monthly_messages = Column(Integer, nullable=False, default=5000)
    
    # WhatsApp Configuration
    whatsapp_phone_number_id = Column(String(255))
    whatsapp_access_token = Column(Text)
    whatsapp_webhook_url = Column(String(500))
    whatsapp_webhook_verify_token = Column(String(255))
    
    settings = Column(JSON, default={})
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(36))
    
    # Relationships
    users = relationship("User", back_populates="clinic", cascade="all, delete-orphan")
    calls = relationship("Call", back_populates="clinic", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="clinic", cascade="all, delete-orphan")
    whatsapp_conversations = relationship("WhatsAppConversation", back_populates="clinic", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="clinic", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="clinic", cascade="all, delete-orphan")
    system_metrics = relationship("SystemMetric", back_populates="clinic", cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        super(Clinic, self).__init__(**kwargs)
        if not self.slug and self.name:
            self.slug = self.name.lower().replace(' ', '-').replace('_', '-')
    
    def to_dict(self, include_sensitive=False):
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'subscription_status': self.subscription_status,
            'subscription_plan': self.subscription_plan,
            'subscription_expires_at': self.subscription_expires_at.isoformat() if self.subscription_expires_at else None,
            'max_users': self.max_users,
            'max_monthly_calls': self.max_monthly_calls,
            'max_monthly_messages': self.max_monthly_messages,
            'settings': self.settings,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_sensitive:
            data.update({
                'whatsapp_phone_number_id': self.whatsapp_phone_number_id,
                'whatsapp_access_token': self.whatsapp_access_token,
                'whatsapp_webhook_url': self.whatsapp_webhook_url,
                'whatsapp_webhook_verify_token': self.whatsapp_webhook_verify_token
            })
        else:
            data.update({
                'whatsapp_configured': bool(self.whatsapp_phone_number_id and self.whatsapp_access_token)
            })
        
        return data
    
    @classmethod
    def create_clinic(cls, name, created_by_user_id, **kwargs):
        """Create a new clinic with default settings"""
        clinic = cls(
            name=name,
            created_by=created_by_user_id,
            **kwargs
        )
        db.session.add(clinic)
        db.session.commit()
        return clinic
    
    def update_whatsapp_config(self, phone_number_id=None, access_token=None, webhook_url=None, verify_token=None):
        """Update WhatsApp configuration for the clinic"""
        if phone_number_id is not None:
            self.whatsapp_phone_number_id = phone_number_id
        if access_token is not None:
            self.whatsapp_access_token = access_token
        if webhook_url is not None:
            self.whatsapp_webhook_url = webhook_url
        if verify_token is not None:
            self.whatsapp_webhook_verify_token = verify_token
        
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def is_subscription_active(self):
        """Check if clinic subscription is active"""
        if self.subscription_status != 'active':
            return False
        
        if self.subscription_expires_at and self.subscription_expires_at < datetime.utcnow():
            return False
        
        return True
    
    def get_usage_stats(self):
        """Get current usage statistics for the clinic"""
        from datetime import datetime, timedelta
        from sqlalchemy import func
        
        # Get current month start
        now = datetime.utcnow()
        month_start = datetime(now.year, now.month, 1)
        
        # Count calls this month
        monthly_calls = db.session.query(func.count(Call.id)).filter(
            Call.clinic_id == self.id,
            Call.created_at >= month_start
        ).scalar() or 0
        
        # Count messages this month
        monthly_messages = db.session.query(func.count(WhatsAppMessage.id)).filter(
            WhatsAppMessage.conversation_id.in_(
                db.session.query(WhatsAppConversation.id).filter(
                    WhatsAppConversation.clinic_id == self.id
                )
            ),
            WhatsAppMessage.created_at >= month_start
        ).scalar() or 0
        
        # Count active users
        active_users = db.session.query(func.count(User.id)).filter(
            User.clinic_id == self.id,
            User.is_active == True
        ).scalar() or 0
        
        return {
            'monthly_calls': monthly_calls,
            'monthly_messages': monthly_messages,
            'active_users': active_users,
            'max_users': self.max_users,
            'max_monthly_calls': self.max_monthly_calls,
            'max_monthly_messages': self.max_monthly_messages,
            'calls_usage_percent': (monthly_calls / self.max_monthly_calls * 100) if self.max_monthly_calls > 0 else 0,
            'messages_usage_percent': (monthly_messages / self.max_monthly_messages * 100) if self.max_monthly_messages > 0 else 0,
            'users_usage_percent': (active_users / self.max_users * 100) if self.max_users > 0 else 0
        }

# Import other models to avoid circular imports
from src.models.call import Call
from src.models.lead import Lead
from src.models.whatsapp import WhatsAppConversation, WhatsAppMessage
from src.models.appointment import Appointment
from src.models.audit import AuditLog, SystemMetric

