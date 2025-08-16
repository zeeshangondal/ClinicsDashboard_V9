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