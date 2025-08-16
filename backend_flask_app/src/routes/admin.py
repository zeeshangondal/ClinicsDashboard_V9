from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User
from src.models.clinic import Clinic
from src.models.audit import AuditLog, SystemMetric
from src.decorators import super_admin_required
from datetime import datetime, timedelta
import logging

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')
logger = logging.getLogger(__name__)

@admin_bp.route('/clinics', methods=['GET'])
@jwt_required()
@super_admin_required
def get_clinics():
    """Get all clinics for super admin"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        status = request.args.get('status', '')
        subscription = request.args.get('subscription', '')
        
        query = Clinic.query
        
        # Apply filters
        if search:
            query = query.filter(Clinic.name.ilike(f'%{search}%'))
        if status:
            query = query.filter(Clinic.status == status)
        if subscription:
            query = query.filter(Clinic.subscription_plan == subscription)
        
        # Order by created date
        query = query.order_by(Clinic.created_at.desc())
        
        # Paginate
        clinics = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'clinics': [clinic.to_dict() for clinic in clinics.items],
            'pagination': {
                'page': page,
                'pages': clinics.pages,
                'per_page': per_page,
                'total': clinics.total
            }
        })
        
    except Exception as e:
        logger.error(f"Error fetching clinics: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to fetch clinics'}), 500

@admin_bp.route('/clinics', methods=['POST'])
@jwt_required()
@super_admin_required
def create_clinic():
    """Create a new clinic"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'subscription_plan', 'admin_email', 'admin_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} is required'}), 400
        
        # Check if clinic name already exists
        if Clinic.query.filter_by(name=data['name']).first():
            return jsonify({'success': False, 'message': 'Clinic name already exists'}), 400
        
        # Create clinic
        clinic = Clinic.create_clinic(
            name=data['name'],
            subscription_plan=data['subscription_plan'],
            admin_email=data['admin_email'],
            admin_name=data['admin_name'],
            admin_password=data.get('admin_password', 'TempPass123!')
        )
        
        # Log the action
        AuditLog.log_action(
            user_id=get_jwt_identity(),
            action='create_clinic',
            resource_type='clinic',
            resource_id=clinic.id,
            details=f"Created clinic: {clinic.name}"
        )
        
        return jsonify({
            'success': True,
            'message': 'Clinic created successfully',
            'clinic': clinic.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating clinic: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to create clinic'}), 500

@admin_bp.route('/clinics/<clinic_id>', methods=['PUT'])
@jwt_required()
@super_admin_required
def update_clinic(clinic_id):
    """Update clinic details"""
    try:
        clinic = Clinic.query.get(clinic_id)
        if not clinic:
            return jsonify({'success': False, 'message': 'Clinic not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['name', 'subscription_plan', 'status', 'settings']
        for field in allowed_fields:
            if field in data:
                setattr(clinic, field, data[field])
        
        clinic.updated_at = datetime.utcnow()
        clinic.save()
        
        # Log the action
        AuditLog.log_action(
            user_id=get_jwt_identity(),
            action='update_clinic',
            resource_type='clinic',
            resource_id=clinic.id,
            details=f"Updated clinic: {clinic.name}"
        )
        
        return jsonify({
            'success': True,
            'message': 'Clinic updated successfully',
            'clinic': clinic.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error updating clinic: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to update clinic'}), 500

@admin_bp.route('/clinics/<clinic_id>', methods=['DELETE'])
@jwt_required()
@super_admin_required
def delete_clinic(clinic_id):
    """Delete a clinic"""
    try:
        clinic = Clinic.query.get(clinic_id)
        if not clinic:
            return jsonify({'success': False, 'message': 'Clinic not found'}), 404
        
        clinic_name = clinic.name
        
        # Soft delete - mark as deleted instead of actually deleting
        clinic.status = 'deleted'
        clinic.deleted_at = datetime.utcnow()
        clinic.save()
        
        # Log the action
        AuditLog.log_action(
            user_id=get_jwt_identity(),
            action='delete_clinic',
            resource_type='clinic',
            resource_id=clinic.id,
            details=f"Deleted clinic: {clinic_name}"
        )
        
        return jsonify({
            'success': True,
            'message': 'Clinic deleted successfully'
        })
        
    except Exception as e:
        logger.error(f"Error deleting clinic: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to delete clinic'}), 500

@admin_bp.route('/system/metrics', methods=['GET'])
@jwt_required()
@super_admin_required
def get_system_metrics():
    """Get system-wide metrics"""
    try:
        # Get current metrics (mock data for now)
        current_metrics = {
            'total_clinics': Clinic.query.count(),
            'active_clinics': Clinic.query.filter_by(status='active').count(),
            'total_users': User.query.count(),
            'system_health': 98.5,
            'uptime_percentage': 99.9
        }
        
        # Get historical data
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        historical_metrics = SystemMetric.query.filter(
            SystemMetric.recorded_at >= start_date
        ).order_by(SystemMetric.recorded_at.desc()).all()
        
        return jsonify({
            'success': True,
            'current_metrics': current_metrics,
            'historical_metrics': [m.to_dict() for m in historical_metrics]
        })
        
    except Exception as e:
        logger.error(f"Error fetching system metrics: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to fetch system metrics'}), 500

@admin_bp.route('/system/logs', methods=['GET'])
@jwt_required()
@super_admin_required
def get_system_logs():
    """Get system audit logs"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        level = request.args.get('level', '')
        category = request.args.get('category', '')
        clinic_id = request.args.get('clinic_id', '')
        
        query = AuditLog.query
        
        # Apply filters
        if level:
            query = query.filter(AuditLog.level == level)
        if category:
            query = query.filter(AuditLog.category == category)
        if clinic_id:
            query = query.filter(AuditLog.clinic_id == clinic_id)
        
        # Order by timestamp
        query = query.order_by(AuditLog.timestamp.desc())
        
        # Paginate
        logs = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'logs': [log.to_dict() for log in logs.items],
            'pagination': {
                'page': page,
                'pages': logs.pages,
                'per_page': per_page,
                'total': logs.total
            }
        })
        
    except Exception as e:
        logger.error(f"Error fetching system logs: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to fetch system logs'}), 500

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@super_admin_required
def get_all_users():
    """Get all users across all clinics"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        role = request.args.get('role', '')
        clinic_id = request.args.get('clinic_id', '')
        
        query = User.query
        
        # Apply filters
        if search:
            query = query.filter(
                User.username.ilike(f'%{search}%') |
                User.email.ilike(f'%{search}%')
            )
        if role:
            query = query.filter(User.role == role)
        if clinic_id:
            query = query.filter(User.clinic_id == clinic_id)
        
        # Order by created date
        query = query.order_by(User.created_at.desc())
        
        # Paginate
        users = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'users': [user.to_dict() for user in users.items],
            'pagination': {
                'page': page,
                'pages': users.pages,
                'per_page': per_page,
                'total': users.total
            }
        })
        
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to fetch users'}), 500

@admin_bp.route('/analytics/usage', methods=['GET'])
@jwt_required()
@super_admin_required
def get_usage_analytics():
    """Get usage analytics across all clinics"""
    try:
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # This would typically involve complex queries across multiple tables
        # For now, return mock data structure
        analytics = {
            'total_calls': 15420,
            'total_messages': 28950,
            'active_clinics': 24,
            'total_users': 156,
            'subscription_distribution': {
                'Premium': 45,
                'Standard': 35,
                'Basic': 15,
                'Trial': 5
            },
            'monthly_growth': [
                {'month': 'Jul', 'clinics': 18, 'calls': 12450, 'messages': 23400},
                {'month': 'Aug', 'clinics': 19, 'calls': 15600, 'messages': 28900},
                {'month': 'Sep', 'clinics': 21, 'calls': 18200, 'messages': 34500},
                {'month': 'Oct', 'clinics': 22, 'calls': 21300, 'messages': 41200},
                {'month': 'Nov', 'clinics': 23, 'calls': 24800, 'messages': 47800},
                {'month': 'Dec', 'clinics': 24, 'calls': 28900, 'messages': 52300}
            ]
        }
        
        return jsonify({
            'success': True,
            'analytics': analytics
        })
        
    except Exception as e:
        logger.error(f"Error fetching usage analytics: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to fetch analytics'}), 500

