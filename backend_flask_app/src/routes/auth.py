from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from src.models.user import User, db
from src.models.clinic import Clinic
from src.models.audit import AuditLog

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT tokens"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    clinic_name = data.get('clinic_name', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not all([clinic_name, username, password]):
        return jsonify({'error': 'Clinic name, username, and password are required'}), 400
    
    try:
        # Handle super admin login (no clinic required)
        if username == 'craft_admin' or clinic_name.lower() == 'craft ai':
            user = User.query.filter_by(username=username, role='super_admin').first()
            if user and user.check_password(password):
                if user.is_locked():
                    return jsonify({'error': 'Account is temporarily locked'}), 423
                
                # Create tokens for super admin
                access_token = create_access_token(
                    identity=user.id,
                    additional_claims={
                        'clinic_id': None,
                        'role': user.role,
                        'permissions': user.permissions or []
                    }
                )
                refresh_token = create_refresh_token(identity=user.id)
                
                # Reset failed login attempts and log successful login
                user.reset_failed_login()
                AuditLog.log_login(
                    user_id=user.id,
                    ip_address=request.remote_addr,
                    user_agent=request.headers.get('User-Agent')
                )
                
                return jsonify({
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': user.to_dict(),
                    'clinic': None
                }), 200
        
        # Find clinic by name
        clinic = Clinic.query.filter_by(name=clinic_name, is_active=True).first()
        if not clinic:
            return jsonify({'error': 'Clinic not found or inactive'}), 404
        
        # Check clinic subscription
        if not clinic.is_subscription_active():
            return jsonify({'error': 'Clinic subscription is not active'}), 403
        
        # Find user in clinic
        user = User.query.filter_by(
            clinic_id=clinic.id,
            username=username,
            is_active=True
        ).first()
        
        if not user or not user.check_password(password):
            # Log failed login attempt
            if user:
                user.increment_failed_login()
            return jsonify({'error': 'Invalid username or password'}), 401
        
        if user.is_locked():
            return jsonify({'error': 'Account is temporarily locked due to failed login attempts'}), 423
        
        # Create JWT tokens
        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                'clinic_id': clinic.id,
                'role': user.role,
                'permissions': user.permissions or []
            }
        )
        refresh_token = create_refresh_token(identity=user.id)
        
        # Reset failed login attempts and log successful login
        user.reset_failed_login()
        AuditLog.log_login(
            user_id=user.id,
            clinic_id=clinic.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict(),
            'clinic': clinic.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Login failed', 'details': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 404
        
        # Get clinic info if user is not super admin
        clinic = None
        if user.clinic_id:
            clinic = Clinic.query.get(user.clinic_id)
            if not clinic or not clinic.is_active or not clinic.is_subscription_active():
                return jsonify({'error': 'Clinic not found or subscription inactive'}), 403
        
        # Create new access token
        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                'clinic_id': clinic.id if clinic else None,
                'role': user.role,
                'permissions': user.permissions or []
            }
        )
        
        return jsonify({
            'access_token': access_token,
            'user': user.to_dict(),
            'clinic': clinic.to_dict() if clinic else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Token refresh failed', 'details': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user and blacklist token"""
    try:
        current_user_id = get_jwt_identity()
        jti = get_jwt()['jti']
        
        # In production, add jti to Redis blacklist
        # For now, we'll just log the logout
        user = User.query.get(current_user_id)
        if user:
            AuditLog.log_logout(
                user_id=user.id,
                clinic_id=user.clinic_id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent')
            )
        
        return jsonify({'message': 'Successfully logged out'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Logout failed', 'details': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get clinic info if user is not super admin
        clinic = None
        if user.clinic_id:
            clinic = Clinic.query.get(user.clinic_id)
        
        return jsonify({
            'user': user.to_dict(),
            'clinic': clinic.to_dict() if clinic else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get user info', 'details': str(e)}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not all([current_password, new_password]):
            return jsonify({'error': 'Current and new passwords are required'}), 400
        
        if not user.check_password(current_password):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        if len(new_password) < 8:
            return jsonify({'error': 'New password must be at least 8 characters long'}), 400
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        # Log password change
        AuditLog.log_action(
            action='update',
            resource_type='user',
            resource_id=user.id,
            clinic_id=user.clinic_id,
            user_id=user.id,
            old_values={'password_changed_at': user.password_changed_at.isoformat()},
            new_values={'password_changed_at': datetime.utcnow().isoformat()},
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to change password', 'details': str(e)}), 500

@auth_bp.route('/verify-token', methods=['POST'])
@jwt_required()
def verify_token():
    """Verify if token is valid"""
    try:
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        
        return jsonify({
            'valid': True,
            'user_id': current_user_id,
            'clinic_id': claims.get('clinic_id'),
            'role': claims.get('role'),
            'permissions': claims.get('permissions', [])
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Token verification failed', 'details': str(e)}), 500

