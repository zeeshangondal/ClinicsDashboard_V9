from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from src.models.user import User

def super_admin_required(f):
    """Decorator to require super admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or user.role != 'super_admin':
            return jsonify({
                'success': False,
                'message': 'Super admin access required'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

def clinic_admin_required(f):
    """Decorator to require clinic admin role or higher"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or user.role not in ['super_admin', 'clinic_admin']:
            return jsonify({
                'success': False,
                'message': 'Clinic admin access required'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

def agent_required(f):
    """Decorator to require agent role or higher"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or user.role not in ['super_admin', 'clinic_admin', 'agent']:
            return jsonify({
                'success': False,
                'message': 'Agent access required'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

def same_clinic_required(f):
    """Decorator to ensure user can only access their own clinic's data"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Super admins can access any clinic's data
        if user.role == 'super_admin':
            return f(*args, **kwargs)
        
        # For other users, add clinic_id to kwargs if not present
        if 'clinic_id' not in kwargs:
            kwargs['clinic_id'] = user.clinic_id
        elif kwargs['clinic_id'] != user.clinic_id:
            return jsonify({
                'success': False,
                'message': 'Access denied to this clinic\'s data'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

