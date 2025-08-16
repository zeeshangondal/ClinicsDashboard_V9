from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, JSON, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
import uuid
from src.models.user import db

class WhatsAppConversation(db.Model):
    __tablename__ = 'whatsapp_conversations'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    clinic_id = Column(String(36), ForeignKey('clinics.id', ondelete='CASCADE'), nullable=False)
    phone_number = Column(String(50), nullable=False)
    contact_name = Column(String(255))
    status = Column(String(50), nullable=False, default='active')
    assigned_agent_id = Column(String(36), ForeignKey('users.id'))
    last_message_at = Column(DateTime)
    last_message_from = Column(String(20))
    unread_count = Column(Integer, default=0)
    is_ai_handled = Column(Boolean, default=True)
    handoff_requested_at = Column(DateTime)
    handoff_reason = Column(Text)
    tags = Column(JSON, default=[])  # Using JSON instead of ARRAY for SQLite compatibility
    conversation_metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    clinic = relationship("Clinic", back_populates="whatsapp_conversations")
    assigned_agent = relationship("User", back_populates="assigned_conversations")
    messages = relationship("WhatsAppMessage", back_populates="conversation", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'clinic_id': self.clinic_id,
            'phone_number': self.phone_number,
            'contact_name': self.contact_name,
            'status': self.status,
            'assigned_agent_id': self.assigned_agent_id,
            'assigned_agent_name': self.assigned_agent.username if self.assigned_agent else None,
            'last_message_at': self.last_message_at.isoformat() if self.last_message_at else None,
            'last_message_from': self.last_message_from,
            'unread_count': self.unread_count,
            'is_ai_handled': self.is_ai_handled,
            'handoff_requested_at': self.handoff_requested_at.isoformat() if self.handoff_requested_at else None,
            'handoff_reason': self.handoff_reason,
            'tags': self.tags or [],
            'metadata': self.conversation_metadata or {},
            'status_color': self.get_status_color(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_status_color(self):
        """Get color indicator for conversation status"""
        status_colors = {
            'active': '#10b981',     # green
            'resolved': '#6b7280',   # gray
            'archived': '#9ca3af',   # light gray
            'escalated': '#ef4444'   # red
        }
        return status_colors.get(self.status, '#6b7280')
    
    def assign_to_agent(self, agent_id, handoff_reason=None):
        """Assign conversation to a human agent"""
        self.assigned_agent_id = agent_id
        self.is_ai_handled = False
        self.handoff_requested_at = datetime.utcnow()
        self.handoff_reason = handoff_reason
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def mark_as_resolved(self):
        """Mark conversation as resolved"""
        self.status = 'resolved'
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def add_tag(self, tag):
        """Add a tag to the conversation"""
        if not self.tags:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.utcnow()
            db.session.commit()
    
    def remove_tag(self, tag):
        """Remove a tag from the conversation"""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow()
            db.session.commit()
    
    def increment_unread(self):
        """Increment unread message count"""
        self.unread_count += 1
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def mark_as_read(self):
        """Mark all messages as read"""
        self.unread_count = 0
        self.updated_at = datetime.utcnow()
        
        # Mark all messages as read
        WhatsAppMessage.query.filter_by(
            conversation_id=self.id,
            is_read=False
        ).update({'is_read': True, 'read_at': datetime.utcnow()})
        
        db.session.commit()
    
    @classmethod
    def get_or_create_conversation(cls, clinic_id, phone_number, contact_name=None):
        """Get existing conversation or create new one"""
        conversation = cls.query.filter_by(
            clinic_id=clinic_id,
            phone_number=phone_number
        ).first()
        
        if not conversation:
            conversation = cls(
                clinic_id=clinic_id,
                phone_number=phone_number,
                contact_name=contact_name
            )
            db.session.add(conversation)
            db.session.commit()
        
        return conversation
    
    def __repr__(self):
        return f'<WhatsAppConversation {self.phone_number} ({self.status})>'


class WhatsAppMessage(db.Model):
    __tablename__ = 'whatsapp_messages'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey('whatsapp_conversations.id', ondelete='CASCADE'), nullable=False)
    external_message_id = Column(String(255))
    sender_type = Column(String(20), nullable=False)
    sender_name = Column(String(255))
    sender_phone = Column(String(50))
    message_type = Column(String(50), nullable=False, default='text')
    content = Column(Text)
    media_url = Column(Text)
    media_type = Column(String(50))
    media_filename = Column(String(255))
    status = Column(String(50), nullable=False, default='sent')
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    delivered_at = Column(DateTime)
    failed_reason = Column(Text)
    message_metadata = Column(JSON, default={})
    sent_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("WhatsAppConversation", back_populates="messages")
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'external_message_id': self.external_message_id,
            'sender_type': self.sender_type,
            'sender_name': self.sender_name,
            'sender_phone': self.sender_phone,
            'message_type': self.message_type,
            'content': self.content,
            'media_url': self.media_url,
            'media_type': self.media_type,
            'media_filename': self.media_filename,
            'status': self.status,
            'is_read': self.is_read,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'failed_reason': self.failed_reason,
            'metadata': self.message_metadata or {},
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'sender_color': self.get_sender_color()
        }
    
    def get_sender_color(self):
        """Get color indicator for message sender"""
        sender_colors = {
            'customer': '#3b82f6',  # blue
            'ai': '#10b981',        # green
            'agent': '#8b5cf6'      # purple
        }
        return sender_colors.get(self.sender_type, '#6b7280')
    
    def mark_as_read(self):
        """Mark message as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.utcnow()
            db.session.commit()
    
    def mark_as_delivered(self):
        """Mark message as delivered"""
        self.status = 'delivered'
        self.delivered_at = datetime.utcnow()
        db.session.commit()
    
    def mark_as_failed(self, reason):
        """Mark message as failed"""
        self.status = 'failed'
        self.failed_reason = reason
        db.session.commit()
    
    @classmethod
    def create_message(cls, conversation_id, sender_type, content, **kwargs):
        """Create a new WhatsApp message"""
        message = cls(
            conversation_id=conversation_id,
            sender_type=sender_type,
            content=content,
            sent_at=datetime.utcnow(),
            **kwargs
        )
        db.session.add(message)
        
        # Update conversation last message info
        conversation = WhatsAppConversation.query.get(conversation_id)
        if conversation:
            conversation.last_message_at = message.sent_at
            conversation.last_message_from = sender_type
            
            # Increment unread count if message is from customer
            if sender_type == 'customer':
                conversation.increment_unread()
        
        db.session.commit()
        return message
    
    def __repr__(self):
        return f'<WhatsAppMessage {self.sender_type}: {self.content[:50]}...>'

