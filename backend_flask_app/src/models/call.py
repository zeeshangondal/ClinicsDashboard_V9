from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from src.models.user import db

class Call(db.Model):
    __tablename__ = 'calls'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    clinic_id = Column(String(36), ForeignKey('clinics.id', ondelete='CASCADE'), nullable=False)
    external_call_id = Column(String(255))
    call_type = Column(String(20), nullable=False)
    direction = Column(String(20), nullable=False)
    phone_number = Column(String(50), nullable=False)
    contact_name = Column(String(255))
    lead_id = Column(String(36), ForeignKey('leads.id'))
    status = Column(String(50), nullable=False)
    duration_seconds = Column(Integer, default=0)
    recording_url = Column(Text)
    transcript = Column(Text)
    ai_summary = Column(Text)
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    clinic = relationship("Clinic", back_populates="calls")
    lead = relationship("Lead", back_populates="calls")
    
    def to_dict(self):
        return {
            'id': self.id,
            'clinic_id': self.clinic_id,
            'external_call_id': self.external_call_id,
            'call_type': self.call_type,
            'direction': self.direction,
            'phone_number': self.phone_number,
            'contact_name': self.contact_name,
            'lead_id': self.lead_id,
            'status': self.status,
            'duration_seconds': self.duration_seconds,
            'duration_formatted': self.format_duration(),
            'recording_url': self.recording_url,
            'transcript': self.transcript,
            'ai_summary': self.ai_summary,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def format_duration(self):
        """Format duration in human-readable format"""
        if not self.duration_seconds:
            return "0:00"
        
        minutes = self.duration_seconds // 60
        seconds = self.duration_seconds % 60
        return f"{minutes}:{seconds:02d}"
    
    def get_status_color(self):
        """Get color indicator for call status"""
        status_colors = {
            'initiated': '#fbbf24',  # yellow
            'ringing': '#3b82f6',    # blue
            'answered': '#10b981',   # green
            'completed': '#059669',  # dark green
            'failed': '#ef4444',     # red
            'busy': '#f59e0b',       # orange
            'no_answer': '#6b7280',  # gray
            'cancelled': '#9ca3af'   # light gray
        }
        return status_colors.get(self.status, '#6b7280')
    
    @classmethod
    def create_call(cls, clinic_id, phone_number, call_type, direction, **kwargs):
        """Create a new call record"""
        call = cls(
            clinic_id=clinic_id,
            phone_number=phone_number,
            call_type=call_type,
            direction=direction,
            status='initiated',
            started_at=datetime.utcnow(),
            **kwargs
        )
        db.session.add(call)
        db.session.commit()
        return call
    
    def update_status(self, status, **kwargs):
        """Update call status and related fields"""
        self.status = status
        self.updated_at = datetime.utcnow()
        
        if status == 'completed' and not self.ended_at:
            self.ended_at = datetime.utcnow()
            if self.started_at:
                self.duration_seconds = int((self.ended_at - self.started_at).total_seconds())
        
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        db.session.commit()
    
    def __repr__(self):
        return f'<Call {self.phone_number} ({self.status})>'

