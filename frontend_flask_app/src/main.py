import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_socketio import SocketIO

from src.config import Config
from src.models.user import db
from src.models.clinic import Clinic
from src.models.call import Call
from src.models.lead import Lead
from src.models.whatsapp import WhatsAppConversation, WhatsAppMessage
from src.models.appointment import Appointment, AppointmentConfirmation
from src.models.audit import AuditLog, SystemMetric

# Import blueprints
from src.routes.auth import auth_bp
from src.routes.admin import admin_bp
# from src.routes.clinic import clinic_bp
# from src.routes.dashboard import dashboard_bp
from src.routes.calls import calls_bp
# from src.routes.leads import leads_bp
# from src.routes.whatsapp import whatsapp_bp
# from src.routes.appointments import appointments_bp

def create_app():
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    cors = CORS(app, origins=app.config['CORS_ORIGINS'])
    socketio = SocketIO(app, cors_allowed_origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    # app.register_blueprint(clinic_bp, url_prefix='/api/clinics')
    # app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(calls_bp, url_prefix="/api/calls")
    # app.register_blueprint(leads_bp, url_prefix='/api/leads')
    # app.register_blueprint(whatsapp_bp, url_prefix='/api/whatsapp')
    # app.register_blueprint(appointments_bp, url_prefix='/api/appointments')
    
    # Create database tables
    # with app.app_context():
    #     db.create_all()
        
    #     # Create default super admin if it doesn't exist
    #     from src.models.user import User
    #     super_admin = User.query.filter_by(role=\'super_admin\').first()
    #     if not super_admin:
    #         try:
    #             User.create_super_admin(
    #                 username=\'craft_admin\',
    #                 email=\'admin@craftai.com\',
    #                 password=\'CraftAI2024!\',
    #                 first_name=\'Craft AI\',
    #                 last_name=\'Administrator\'
    #             )
    #             print("✅ Default super admin created: craft_admin / CraftAI2024!")
    #         except Exception as e:
    #             print(f"❌ Error creating super admin: {e}")
        
    #     # Create demo clinic and user if they don't exist
    #     demo_clinic = Clinic.query.filter_by(name=\'Demo Clinic\').first()
    #     if not demo_clinic:
    #         try:
    #             demo_clinic = Clinic(
    #                 name=\'Demo Clinic\',
    #                 is_active=True,
    #                 subscription_status=\'active\',
    #                 subscription_plan=\'basic\'
    #             )
    #             db.session.add(demo_clinic)
    #             db.session.commit()
    #             print(f"✅ Demo Clinic created with ID: {demo_clinic.id}")
    #         except Exception as e:
    #             print(f"❌ Error creating demo clinic: {e}")
        
    #     # Create demo user if it doesn't exist
    #     if demo_clinic:
    #         demo_user = User.query.filter_by(username=\'demo\', clinic_id=demo_clinic.id).first()
    #         if not demo_user:
    #             try:
    #                 demo_user = User.create_user(
    #                     clinic_id=demo_clinic.id,
    #                     username=\'demo\',
    #                     email=\'demo@example.com\',
    #                     password=\'demo\',
    #                     role=\'admin\',
    #                     first_name=\'Demo\',
    #                     last_name=\'User\'
    #                 )
    #                 print(f"✅ Demo user created with ID: {demo_user.id}")
    #             except Exception as e:
    #                 print(f"❌ Error creating demo user: {e}")
    
    # JWT token blacklist (in production, use Redis)
    blacklisted_tokens = set()
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return jwt_payload['jti'] in blacklisted_tokens
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return {'message': 'Token has been revoked'}, 401
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'message': 'Token has expired'}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'message': 'Invalid token'}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'message': 'Authorization token is required'}, 401
    
    # Serve static assets
    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        return send_from_directory(os.path.join(app.static_folder, 'assets'), filename)
    
    # Serve React frontend for all non-API routes
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        if path.startswith("api/"):
            return "Not Found", 404 # Or handle API routes separately if needed
        try:
            return send_from_directory(app.static_folder, path)
        except:
            return send_from_directory(app.static_folder, "index.html")
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Craft AI Dashboard API is running'}
    
    return app, socketio

app, socketio = create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

