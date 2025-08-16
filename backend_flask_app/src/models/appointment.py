from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from src.models.user import db

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    clinic_id = Column(String(36), ForeignKey('clinics.id', ondelete='CASCADE'), nullable=False)
    patient_name = Column(String(255), nullable=False)
    patient_phone = Column(String(50), nullable=False)
    patient_email = Column(String(255))
    appointment_type = Column(String(100))
    appointment_date = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=30)
    status = Column(String(50), nullable=False, default='scheduled')
    confirmation_status = Column(String(50), nullable=False, default='pending')
    confirmation_method = Column(String(50))
    confirmed_at = Column(DateTime)
    cancelled_at = Column(DateTime)
    cancellation_reason = Column(Text)
    reschedule_count = Column(Integer, default=0)
    original_appointment_date = Column(DateTime)
    reminder_sent_at = Column(DateTime)
    notes = Column(Text)
    assigned_provider = Column(String(255))
    created_by = Column(String(36), ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    clinic = relationship("Clinic", back_populates="appointments")
    created_by_user = relationship("User", back_populates="created_appointments")
    confirmations = relationship("AppointmentConfirmation", back_populates="appointment", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'clinic_id': self.clinic_id,
            'patient_name': self.patient_name,
            'patient_phone': self.patient_phone,
            'patient_email': self.patient_email,
            'appointment_type': self.appointment_type,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'duration_minutes': self.duration_minutes,
            'status': self.status,
            'confirmation_status': self.confirmation_status,
            'confirmation_method': self.confirmation_method,
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
            'cancellation_reason': self.cancellation_reason,
            'reschedule_count': self.reschedule_count,
            'original_appointment_date': self.original_appointment_date.isoformat() if self.original_appointment_date else None,
            'reminder_sent_at': self.reminder_sent_at.isoformat() if self.reminder_sent_at else None,
            'notes': self.notes,
            'assigned_provider': self.assigned_provider,
            'created_by': self.created_by,
            'created_by_name': self.created_by_user.username if self.created_by_user else None,
            'status_color': self.get_status_color(),
            'confirmation_color': self.get_confirmation_color(),
            'is_upcoming': self.is_upcoming(),
            'is_overdue': self.is_overdue(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_status_color(self):
        """Get color indicator for appointment status"""
        status_colors = {
            'scheduled': '#3b82f6',    # blue
            'confirmed': '#10b981',    # green
            'completed': '#059669',    # dark green
            'cancelled': '#ef4444',    # red
            'no_show': '#f59e0b',      # orange
            'rescheduled': '#8b5cf6'   # purple
        }
        return status_colors.get(self.status, '#6b7280')
    
    def get_confirmation_color(self):
        """Get color indicator for confirmation status"""
        confirmation_colors = {
            'pending': '#f59e0b',      # orange
            'confirmed': '#10b981',    # green
            'declined': '#ef4444',     # red
            'no_response': '#6b7280'   # gray
        }
        return confirmation_colors.get(self.confirmation_status, '#6b7280')
    
    def is_upcoming(self):
        """Check if appointment is upcoming"""
        return self.appointment_date > datetime.utcnow() and self.status in ['scheduled', 'confirmed']
    
    def is_overdue(self):
        """Check if appointment is overdue"""
        return self.appointment_date < datetime.utcnow() and self.status in ['scheduled', 'confirmed']
    
    def confirm_appointment(self, method='manual', notes=None):
        """Confirm the appointment"""
        self.status = 'confirmed'
        self.confirmation_status = 'confirmed'
        self.confirmation_method = method
        self.confirmed_at = datetime.utcnow()
        if notes:
            self.notes = notes
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def cancel_appointment(self, reason=None, cancelled_by='patient'):
        """Cancel the appointment"""
        self.status = 'cancelled'
        self.confirmation_status = 'declined'
        self.cancelled_at = datetime.utcnow()
        self.cancellation_reason = reason or f"Cancelled by {cancelled_by}"
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def reschedule_appointment(self, new_date, reason=None):
        """Reschedule the appointment"""
        if not self.original_appointment_date:
            self.original_appointment_date = self.appointment_date
        
        self.appointment_date = new_date
        self.status = 'rescheduled'
        self.confirmation_status = 'pending'
        self.reschedule_count += 1
        if reason:
            if self.notes:
                self.notes += f"\n\nRescheduled: {reason}"
            else:
                self.notes = f"Rescheduled: {reason}"
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def mark_as_no_show(self):
        """Mark appointment as no show"""
        self.status = 'no_show'
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def mark_as_completed(self, notes=None):
        """Mark appointment as completed"""
        self.status = 'completed'
        if notes:
            if self.notes:
                self.notes += f"\n\nCompleted: {notes}"
            else:
                self.notes = f"Completed: {notes}"
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def send_reminder(self):
        """Mark reminder as sent"""
        self.reminder_sent_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    @classmethod
    def create_appointment(cls, clinic_id, patient_name, patient_phone, appointment_date, **kwargs):
        """Create a new appointment"""
        appointment = cls(
            clinic_id=clinic_id,
            patient_name=patient_name,
            patient_phone=patient_phone,
            appointment_date=appointment_date,
            **kwargs
        )
        db.session.add(appointment)
        db.session.commit()
        return appointment
    
    def __repr__(self):
        return f'<Appointment {self.patient_name} on {self.appointment_date}>'


class AppointmentConfirmation(db.Model):
    __tablename__ = 'appointment_confirmations'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    appointment_id = Column(String(36), ForeignKey('appointments.id', ondelete='CASCADE'), nullable=False)
    confirmation_method = Column(String(50), nullable=False)
    message_sent = Column(Text)
    response_received = Column(Text)
    response_type = Column(String(50))
    responded_at = Column(DateTime)
    sent_at = Column(DateTime, nullable=False)
    external_message_id = Column(String(255))
    status = Column(String(50), nullable=False, default='sent')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    appointment = relationship("Appointment", back_populates="confirmations")
    
    def to_dict(self):
        return {
            'id': self.id,
            'appointment_id': self.appointment_id,
            'confirmation_method': self.confirmation_method,
            'message_sent': self.message_sent,
            'response_received': self.response_received,
            'response_type': self.response_type,
            'responded_at': self.responded_at.isoformat() if self.responded_at else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'external_message_id': self.external_message_id,
            'status': self.status,
            'status_color': self.get_status_color(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def get_status_color(self):
        """Get color indicator for confirmation status"""
        status_colors = {
            'sent': '#f59e0b',        # orange
            'delivered': '#3b82f6',   # blue
            'responded': '#10b981',   # green
            'failed': '#ef4444'       # red
        }
        return status_colors.get(self.status, '#6b7280')
    
    def record_response(self, response_text, response_type):
        """Record patient response to confirmation"""
        self.response_received = response_text
        self.response_type = response_type
        self.responded_at = datetime.utcnow()
        self.status = 'responded'
        
        # Update appointment based on response
        if response_type == 'confirmed':
            self.appointment.confirm_appointment(method=self.confirmation_method)
        elif response_type == 'cancelled':
            self.appointment.cancel_appointment(reason="Patient cancelled via confirmation")
        
        db.session.commit()
    
    @classmethod
    def create_confirmation(cls, appointment_id, method, message_sent, **kwargs):
        """Create a new appointment confirmation"""
        confirmation = cls(
            appointment_id=appointment_id,
            confirmation_method=method,
            message_sent=message_sent,
            sent_at=datetime.utcnow(),
            **kwargs
        )
        db.session.add(confirmation)
        db.session.commit()
        return confirmation
    
    def __repr__(self):
        return f'<AppointmentConfirmation {self.confirmation_method} ({self.status})>'

