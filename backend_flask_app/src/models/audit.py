from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, ForeignKey, Numeric
from sqlalchemy.orm import relationship
import uuid
from src.models.user import db

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    clinic_id = Column(String(36), ForeignKey('clinics.id', ondelete='CASCADE'))
    user_id = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(String(36))
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(45))  # IPv6 compatible
    user_agent = Column(Text)
    session_id = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    clinic = relationship("Clinic", back_populates="audit_logs")
    user = relationship("User", back_populates="audit_logs")
    
    def to_dict(self):
        return {
            'id': self.id,
            'clinic_id': self.clinic_id,
            'user_id': self.user_id,
            'user_name': self.user.username if self.user else None,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'old_values': self.old_values,
            'new_values': self.new_values,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'session_id': self.session_id,
            'action_color': self.get_action_color(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def get_action_color(self):
        """Get color indicator for audit action"""
        action_colors = {
            'create': '#10b981',    # green
            'read': '#3b82f6',      # blue
            'update': '#f59e0b',    # orange
            'delete': '#ef4444',    # red
            'login': '#8b5cf6',     # purple
            'logout': '#6b7280',    # gray
            'export': '#f59e0b',    # orange
            'import': '#10b981'     # green
        }
        return action_colors.get(self.action, '#6b7280')
    
    @classmethod
    def log_action(cls, action, resource_type, resource_id=None, old_values=None, new_values=None, 
                   clinic_id=None, user_id=None, ip_address=None, user_agent=None, session_id=None):
        """Create an audit log entry"""
        audit_log = cls(
            clinic_id=clinic_id,
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id
        )
        db.session.add(audit_log)
        db.session.commit()
        return audit_log
    
    @classmethod
    def log_login(cls, user_id, clinic_id=None, ip_address=None, user_agent=None, session_id=None):
        """Log user login"""
        return cls.log_action(
            action='login',
            resource_type='user',
            resource_id=user_id,
            clinic_id=clinic_id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id
        )
    
    @classmethod
    def log_logout(cls, user_id, clinic_id=None, ip_address=None, user_agent=None, session_id=None):
        """Log user logout"""
        return cls.log_action(
            action='logout',
            resource_type='user',
            resource_id=user_id,
            clinic_id=clinic_id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id
        )
    
    def __repr__(self):
        return f'<AuditLog {self.action} {self.resource_type}>'


class SystemMetric(db.Model):
    __tablename__ = 'system_metrics'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    clinic_id = Column(String(36), ForeignKey('clinics.id', ondelete='CASCADE'))
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Numeric, nullable=False)
    metric_unit = Column(String(50))
    dimensions = Column(JSON, default={})
    recorded_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    clinic = relationship("Clinic", back_populates="system_metrics")
    
    def to_dict(self):
        return {
            'id': self.id,
            'clinic_id': self.clinic_id,
            'metric_name': self.metric_name,
            'metric_value': float(self.metric_value),
            'metric_unit': self.metric_unit,
            'dimensions': self.dimensions or {},
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def record_metric(cls, metric_name, metric_value, clinic_id=None, metric_unit=None, 
                     dimensions=None, recorded_at=None):
        """Record a system metric"""
        if recorded_at is None:
            recorded_at = datetime.utcnow()
        
        metric = cls(
            clinic_id=clinic_id,
            metric_name=metric_name,
            metric_value=metric_value,
            metric_unit=metric_unit,
            dimensions=dimensions or {},
            recorded_at=recorded_at
        )
        db.session.add(metric)
        db.session.commit()
        return metric
    
    @classmethod
    def record_call_metric(cls, clinic_id, call_count, call_duration_total=None):
        """Record call-related metrics"""
        metrics = []
        
        # Record call count
        metrics.append(cls.record_metric(
            metric_name='calls_count',
            metric_value=call_count,
            clinic_id=clinic_id,
            metric_unit='count'
        ))
        
        # Record call duration if provided
        if call_duration_total is not None:
            metrics.append(cls.record_metric(
                metric_name='calls_duration_total',
                metric_value=call_duration_total,
                clinic_id=clinic_id,
                metric_unit='seconds'
            ))
        
        return metrics
    
    @classmethod
    def record_message_metric(cls, clinic_id, message_count, message_type=None):
        """Record WhatsApp message metrics"""
        dimensions = {}
        if message_type:
            dimensions['message_type'] = message_type
        
        return cls.record_metric(
            metric_name='whatsapp_messages_count',
            metric_value=message_count,
            clinic_id=clinic_id,
            metric_unit='count',
            dimensions=dimensions
        )
    
    @classmethod
    def record_appointment_metric(cls, clinic_id, appointment_count, appointment_status=None):
        """Record appointment-related metrics"""
        dimensions = {}
        if appointment_status:
            dimensions['status'] = appointment_status
        
        return cls.record_metric(
            metric_name='appointments_count',
            metric_value=appointment_count,
            clinic_id=clinic_id,
            metric_unit='count',
            dimensions=dimensions
        )
    
    @classmethod
    def record_user_activity_metric(cls, clinic_id, active_users_count):
        """Record user activity metrics"""
        return cls.record_metric(
            metric_name='active_users_count',
            metric_value=active_users_count,
            clinic_id=clinic_id,
            metric_unit='count'
        )
    
    def __repr__(self):
        return f'<SystemMetric {self.metric_name}: {self.metric_value}>'

