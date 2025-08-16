#!/usr/bin/env python3
"""
Script to seed demo data for calls with different reasons
"""
from datetime import datetime, timedelta
import random
from src.main import app
from src.models.call import Call
from src.models.clinic import Clinic
from src.models.user import User, db

def create_demo_calls():
    """Create demo calls with various reasons for testing"""
    with app.app_context():
        try:
            # Get demo clinic
            demo_clinic = Clinic.query.filter_by(name='Demo Clinic').first()
            if not demo_clinic:
                print("❌ Demo Clinic not found")
                return False
            
            # Call reasons to create
            call_reasons = [
                "Birthday Call",
                "Appointment Confirmation", 
                "Booking Call",
                "Follow-up Call",
                "Consultation Call",
                "Reminder Call",
                "Sales Call",
                "Support Call",
                "General Inquiry",
                "Billing Inquiry"
            ]
            
            # Phone numbers and contact names for demo
            contacts = [
                ("+1234567890", "John Smith"),
                ("+1234567891", "Jane Doe"),
                ("+1234567892", "Mike Johnson"),
                ("+1234567893", "Sarah Wilson"),
                ("+1234567894", "David Brown"),
                ("+1234567895", "Lisa Davis"),
                ("+1234567896", "Tom Anderson"),
                ("+1234567897", "Emily Garcia"),
                ("+1234567898", "Chris Martinez"),
                ("+1234567899", "Amanda Taylor")
            ]
            
            # Create calls for the past 30 days
            for i in range(50):  # Create 50 demo calls
                # Random date within last 30 days
                days_ago = random.randint(0, 30)
                hours_ago = random.randint(0, 23)
                minutes_ago = random.randint(0, 59)
                
                started_at = datetime.utcnow() - timedelta(
                    days=days_ago, 
                    hours=hours_ago, 
                    minutes=minutes_ago
                )
                
                # Random call duration (30 seconds to 10 minutes)
                duration = random.randint(30, 600)
                ended_at = started_at + timedelta(seconds=duration)
                
                # Random contact
                phone_number, contact_name = random.choice(contacts)
                
                # Random call reason (stored in call_type field)
                call_reason = random.choice(call_reasons)
                
                # Random direction (more outbound for this demo)
                direction = random.choices(["outbound", "inbound"], weights=[70, 30])[0]
                
                # Random status
                status = random.choices(
                    ["completed", "failed", "no_answer", "busy"], 
                    weights=[70, 10, 15, 5]
                )[0]
                
                # Create the call
                call = Call(
                    clinic_id=demo_clinic.id,
                    call_type=call_reason,  # Using call_type field to store call reason
                    direction=direction,
                    phone_number=phone_number,
                    contact_name=contact_name,
                    status=status,
                    duration_seconds=duration if status == "completed" else 0,
                    started_at=started_at,
                    ended_at=ended_at if status == "completed" else None,
                    ai_summary=f"Demo {call_reason.lower()} call with {contact_name}" if status == "completed" else None
                )
                
                db.session.add(call)
            
            db.session.commit()
            print(f"✅ Created 50 demo calls with various reasons")
            
            # Print summary
            for call_reason in call_reasons:
                count = Call.query.filter_by(
                    clinic_id=demo_clinic.id, 
                    call_type=call_reason
                ).count()
                print(f"  - {call_reason}: {count} calls")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating demo calls: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    create_demo_calls()

