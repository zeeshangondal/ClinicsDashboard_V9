from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from src.models.user import db

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    clinic_id = Column(String(36), ForeignKey('clinics.id', ondelete='CASCADE'), nullable=False)
    phone_number = Column(String(50), nullable=False)
    name = Column(String(255))
    email = Column(String(255))
    status = Column(String(50), nullable=False, default='new')
    priority = Column(String(20), nullable=False, default='medium')
    source = Column(String(100))
    notes = Column(Text)
    lead_metadata = Column(JSON, default={})
    last_contacted_at = Column(DateTime)
    next_contact_at = Column(DateTime)
    assigned_to = Column(String(36), ForeignKey('users.id'))
    call_attempts = Column(Integer, default=0)
    max_call_attempts = Column(Integer, default=3)
    do_not_call = Column(Boolean, default=False)
    do_not_call_reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    clinic = relationship("Clinic", back_populates="leads")
    assigned_user = relationship("User", back_populates="assigned_leads")
    calls = relationship("Call", back_populates="lead")
    
    def to_dict(self):
        return {
            'id': self.id,
            'clinic_id': self.clinic_id,
            'phone_number': self.phone_number,
            'name': self.name,
            'email': self.email,
            'status': self.status,
            'priority': self.priority,
            'source': self.source,
            'notes': self.notes,
            'metadata': self.lead_metadata,
            'last_contacted_at': self.last_contacted_at.isoformat() if self.last_contacted_at else None,
            'next_contact_at': self.next_contact_at.isoformat() if self.next_contact_at else None,
            'assigned_to': self.assigned_to,
            'assigned_user_name': self.assigned_user.username if self.assigned_user else None,
            'call_attempts': self.call_attempts,
            'max_call_attempts': self.max_call_attempts,
            'do_not_call': self.do_not_call,
            'do_not_call_reason': self.do_not_call_reason,
            'status_color': self.get_status_color(),
            'priority_color': self.get_priority_color(),
            'can_call': self.can_call(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_status_color(self):
        """Get color indicator for lead status"""
        status_colors = {
            'new': '#3b82f6',           # blue
            'contacted': '#f59e0b',     # orange
            'interested': '#10b981',    # green
            'not_interested': '#6b7280', # gray
            'callback': '#8b5cf6',      # purple
            'converted': '#059669',     # dark green
            'do_not_call': '#ef4444'    # red
        }
        return status_colors.get(self.status, '#6b7280')
    
    def get_priority_color(self):
        """Get color indicator for lead priority"""
        priority_colors = {
            'low': '#6b7280',      # gray
            'medium': '#f59e0b',   # orange
            'high': '#ef4444',     # red
            'urgent': '#dc2626'    # dark red
        }
        return priority_colors.get(self.priority, '#6b7280')
    
    def can_call(self):
        """Check if lead can be called"""
        if self.do_not_call:
            return False
        if self.call_attempts >= self.max_call_attempts:
            return False
        if self.status == 'do_not_call':
            return False
        return True
    
    def mark_as_do_not_call(self, reason=None):
        """Mark lead as do not call"""
        self.do_not_call = True
        self.status = 'do_not_call'
        self.do_not_call_reason = reason
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def update_status(self, status, notes=None):
        """Update lead status"""
        self.status = status
        if notes:
            if self.notes:
                self.notes += f"\n\n{datetime.utcnow().strftime('%Y-%m-%d %H:%M')}: {notes}"
            else:
                self.notes = f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M')}: {notes}"
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def increment_call_attempt(self):
        """Increment call attempts"""
        self.call_attempts += 1
        self.last_contacted_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def assign_to_user(self, user_id):
        """Assign lead to a user"""
        self.assigned_to = user_id
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    @classmethod
    def create_lead(cls, clinic_id, phone_number, **kwargs):
        """Create a new lead"""
        # Check if lead already exists for this clinic
        existing_lead = cls.query.filter_by(clinic_id=clinic_id, phone_number=phone_number).first()
        if existing_lead:
            raise ValueError("Lead with this phone number already exists")
        
        lead = cls(
            clinic_id=clinic_id,
            phone_number=phone_number,
            **kwargs
        )
        db.session.add(lead)
        db.session.commit()
        return lead
    
    @classmethod
    def bulk_create_leads(cls, clinic_id, leads_data):
        """Create multiple leads from a list"""
        created_leads = []
        errors = []
        
        for lead_data in leads_data:
            try:
                lead = cls.create_lead(clinic_id, **lead_data)
                created_leads.append(lead)
            except Exception as e:
                errors.append({
                    'phone_number': lead_data.get('phone_number'),
                    'error': str(e)
                })
        
        return created_leads, errors
    
    def __repr__(self):
        return f'<Lead {self.phone_number} ({self.status})>'

