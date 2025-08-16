from src.models.user import db, User
from src.models.clinic import Clinic
from src.models.call import Call
from src.models.lead import Lead
from src.models.whatsapp import WhatsAppConversation, WhatsAppMessage
from src.models.appointment import Appointment, AppointmentConfirmation
from src.models.audit import AuditLog, SystemMetric
from datetime import datetime, timedelta
from src.main import create_app # Import create_app from your main Flask app file

def seed_data():
    """Seeds the database with initial demo data."""
    # Ensure application context is available for DB operations
    # Note: create_app() itself might call db.create_all(), so we need
    # to make sure the app context is established for subsequent db operations within this function.
    print("Attempting to seed database...")
    try:
        with db.session.begin(): # Use a transaction for all seeding operations
            # Create default super admin if it doesn't exist
            super_admin = User.query.filter_by(role='super_admin').first()
            if not super_admin:
                User.create_super_admin(
                    username='craft_admin',
                    email='admin@craftai.com',
                    password='CraftAI2024!',
                    first_name='Craft AI',
                    last_name='Administrator'
                )
                db.session.flush() # Flush to make the new super_admin available for queries
                super_admin = User.query.filter_by(username='craft_admin').first() # Re-fetch to ensure it's in session with ID
                print("✅ Default super admin created: craft_admin / CraftAI2024!")

            # Create demo clinic if it doesn't exist
            demo_clinic = Clinic.query.filter_by(name='Dental Access Clinic').first()
            if not demo_clinic:
                demo_clinic = Clinic(
                    name='Dental Access Clinic',
                    address='456 Elm St, Anytown, USA',
                    phone='555-987-6543',
                    email='info@dentalaccess.com',
                    subscription_status='active',
                    subscription_plan='premium'
                )
                db.session.add(demo_clinic)
                db.session.flush() # To get clinic ID for user
                print(f"✅ Demo Clinic created: {demo_clinic.name}")

            # Create primary demo account for Dental Access Clinic if it doesn't exist
            dental_admin = User.query.filter_by(clinic=demo_clinic, username='admin', role='clinic_admin').first()
            if not dental_admin:
                User.create_user(
                    clinic_id=demo_clinic.id,
                    username='admin',
                    email='admin@dentalaccess.com',
                    password='admin123',
                    first_name='Clinic',
                    last_name='Admin',
                    role='clinic_admin',
                    permissions=['manage_users', 'view_reports', 'manage_calls', 'manage_whatsapp', 'manage_appointments']
                )
                db.session.flush()
                dental_admin = User.query.filter_by(clinic=demo_clinic, username='admin').first()
                print(f"✅ Dental Access Clinic primary admin created: admin / admin123")


            # Create secondary demo clinic if it doesn't exist
            medcare_clinic = Clinic.query.filter_by(name='MedCare Clinic').first()
            if not medcare_clinic:
                medcare_clinic = Clinic(
                    name='MedCare Clinic',
                    address='789 Oak Ave, Otherville, USA',
                    phone='555-234-5678',
                    email='info@medcare.com',
                    subscription_status='active',
                    subscription_plan='standard'
                )
                db.session.add(medcare_clinic)
                db.session.flush()
                print(f"✅ Secondary Demo Clinic created: {medcare_clinic.name}")

            # Create secondary demo account for MedCare Clinic
            medcare_admin = User.query.filter_by(clinic=medcare_clinic, username='admin', role='clinic_admin').first()
            if not medcare_admin:
                User.create_user(
                    clinic_id=medcare_clinic.id,
                    username='admin',
                    email='admin@medcare.com',
                    password='password123',
                    first_name='MedCare',
                    last_name='Admin',
                    role='clinic_admin',
                    permissions=['view_reports', 'manage_calls', 'manage_whatsapp']
                )
                db.session.flush()
                print(f"✅ MedCare Clinic admin created: admin / password123")

            # Create Craft AI Internal Use admin account if it doesn't exist
            craftai_clinic = Clinic.query.filter_by(name='Craft AI Solutions').first()
            if not craftai_clinic:
                craftai_clinic = Clinic(
                    name='Craft AI Solutions',
                    address='101 Tech Rd, Innovation City',
                    phone='555-000-1111',
                    email='info@craftai.com',
                    subscription_status='active',
                    subscription_plan='enterprise'
                )
                db.session.add(craftai_clinic)
                db.session.flush()
                print(f"✅ Internal Craft AI Clinic created: {craftai_clinic.name}")

            craftai_internal_admin = User.query.filter_by(clinic=craftai_clinic, username='admin', role='clinic_admin').first()
            if not craftai_internal_admin:
                User.create_user(
                    clinic_id=craftai_clinic.id,
                    username='admin',
                    email='internal@craftai.com',
                    password='craftai2024',
                    first_name='Craft AI Internal',
                    last_name='Admin',
                    role='clinic_admin',
                    permissions=['manage_users', 'view_reports', 'manage_calls', 'manage_whatsapp', 'manage_appointments', 'manage_clinic_settings']
                )
                db.session.flush()
                print(f"✅ Craft AI Internal admin created: admin / craftai2024")


            # Example Data for Dental Access Clinic (using dental_admin and demo_clinic)
            if not Call.query.filter_by(clinic=demo_clinic).first():
                now = datetime.utcnow()
                call1_time = now - timedelta(days=5, hours=2)
                call2_time = now - timedelta(days=3, hours=1)
                call3_time = now - timedelta(hours=6)

                call1 = Call(
                    clinic_id=demo_clinic.id,
                    phone_number='+15551234001',
                    contact_name='Patient A',
                    call_type='inbound',
                    direction='inbound',
                    status='completed',
                    duration_seconds=120,
                    transcript='Hello, I need to schedule an appointment for a cleaning.',
                    ai_summary='Patient scheduled for a dental cleaning.',
                    started_at=call1_time,
                    ended_at=call1_time + timedelta(seconds=120)
                )
                db.session.add(call1)

                call2 = Call(
                    clinic_id=demo_clinic.id,
                    phone_number='+15551234002',
                    contact_name='Patient B',
                    call_type='outbound',
                    direction='outbound',
                    status='no_answer',
                    started_at=call2_time
                )
                db.session.add(call2)

                call3 = Call(
                    clinic_id=demo_clinic.id,
                    phone_number='+15551234003',
                    contact_name='Patient C',
                    call_type='inbound',
                    direction='inbound',
                    status='in_progress',
                    started_at=call3_time
                )
                db.session.add(call3)
                print("✅ Example Call data created!")

            if not Lead.query.filter_by(clinic=demo_clinic).first():
                lead1 = Lead(
                    clinic_id=demo_clinic.id,
                    name='New Patient Lead',
                    contact_info={'email': 'newpatient@example.com', 'phone': '555-555-1212'},
                    status='new',
                    source='website',
                    metadata={'notes': 'Interested in dental implants'}
                )
                db.session.add(lead1)
                print("✅ Example Lead created!")

            if not WhatsAppConversation.query.filter_by(clinic=demo_clinic).first():
                wa_conv1 = WhatsAppConversation(clinic_id=demo_clinic.id, contact_name='Jane Smith', contact_phone='987-654-3210', status='open', last_message_at=datetime.utcnow() - timedelta(minutes=10))
                db.session.add(wa_conv1)
                db.session.flush() # To get conversation ID for message

                wa_msg1 = WhatsAppMessage(conversation_id=wa_conv1.id, sender='AI', message='Hello, how can I help you?', timestamp=datetime.utcnow() - timedelta(minutes=10))
                db.session.add(wa_msg1)
                wa_msg2 = WhatsAppMessage(conversation_id=wa_conv1.id, sender='User', message='I want to book an appointment.', timestamp=datetime.utcnow() - timedelta(minutes=8))
                db.session.add(wa_msg2)
                print("✅ Example WhatsApp Conversation and Messages created!")

            if not Appointment.query.filter_by(clinic=demo_clinic).first():
                app1_date = datetime.utcnow() + timedelta(days=7, hours=10)
                app1 = Appointment(
                    clinic_id=demo_clinic.id,
                    patient_name='Alice Brown',
                    patient_phone='+15551234004',
                    appointment_type='Check-up',
                    appointment_date=app1_date,
                    status='scheduled',
                    confirmation_status='pending'
                )
                db.session.add(app1)
                db.session.flush() # To get appointment ID for confirmation

                conf1_time = datetime.utcnow() - timedelta(days=1)
                conf1 = AppointmentConfirmation(
                    appointment_id=app1.id,
                    confirmation_method='whatsapp',
                    message_sent='Your appointment is confirmed.',
                    status='responded',
                    response_received='Yes, I will be there.',
                    response_type='confirmed',
                    sent_at=conf1_time,
                    responded_at=conf1_time + timedelta(hours=1)
                )
                db.session.add(conf1)
                print("✅ Example Appointment and Confirmation created!")

            if not AuditLog.query.first():
                # Ensure super_admin exists before using its ID
                current_super_admin = User.query.filter_by(role='super_admin').first()
                if current_super_admin:
                    audit1 = AuditLog(clinic_id=demo_clinic.id, user_id=current_super_admin.id, action='LOGIN', resource_type='User', resource_id=current_super_admin.id, ip_address='127.0.0.1', user_agent='Mozilla/5.0', session_id='test_session_1')
                    db.session.add(audit1)
                    print("✅ Example Audit Log created!")

            if not SystemMetric.query.first():
                metric1 = SystemMetric(clinic_id=demo_clinic.id, metric_name='login_success', metric_value=10, metric_unit='count')
                db.session.add(metric1)
                metric2 = SystemMetric(clinic_id=demo_clinic.id, metric_name='api_calls', metric_value=100, metric_unit='count')
                db.session.add(metric2)
                print("✅ Example System Metrics created!")

        db.session.commit() # Commit the outer transaction
        print("Database seeding complete!")

    except Exception as e:
        print(f"❌ An error occurred during seeding: {e}")
        # db.session.rollback() # This rollback is handled by the 'with db.session.begin():' block if an exception occurs
        import traceback
        traceback.print_exc() # Print full traceback for debugging


if __name__ == '__main__':
    # Initialize the Flask app and create an application context
    app = create_app()
    with app.app_context():
        seed_data()