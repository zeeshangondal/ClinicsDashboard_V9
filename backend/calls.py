from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.call import Call
from src.models.clinic import Clinic
from src.models.user import User
from src.decorators import same_clinic_required

calls_bp = Blueprint("calls", __name__)

@calls_bp.route("/", methods=["GET"])
@jwt_required()
@same_clinic_required
def get_calls():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 404

        clinic_id = user.clinic_id
        
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        direction = request.args.get("direction", None)
        call_reason = request.args.get("call_reason", None)
        search_query = request.args.get("search", None)

        query = Call.query.filter_by(clinic_id=clinic_id)

        if direction:
            query = query.filter_by(direction=direction)
        if call_reason:
            query = query.filter_by(call_type=call_reason)
        if search_query:
            query = query.filter(Call.phone_number.ilike(f"%{search_query}%") | Call.contact_name.ilike(f"%{search_query}%"))

        calls = query.order_by(Call.started_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            "calls": [call.to_dict() for call in calls.items],
            "total_pages": calls.pages,
            "current_page": calls.page,
            "total_calls": calls.total
        }), 200

    except Exception as e:
        return jsonify({"message": "Error fetching calls", "error": str(e)}), 500

@calls_bp.route("/<call_id>", methods=["GET"])
@jwt_required()
@same_clinic_required
def get_call_details(call_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 404

        clinic_id = user.clinic_id

        call = Call.query.filter_by(id=call_id, clinic_id=clinic_id).first()

        if not call:
            return jsonify({"message": "Call not found"}), 404

        return jsonify(call.to_dict()), 200

    except Exception as e:
        return jsonify({"message": "Error fetching call details", "error": str(e)}), 500

@calls_bp.route("/reasons", methods=["GET"])
@jwt_required()
@same_clinic_required
def get_call_reasons():
    # This is a placeholder. In a real app, call reasons might come from a config or a dedicated table.
    # For now, we'll return a static list of common call reasons.
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
        "Billing Inquiry",
        "Other"
    ]
    return jsonify({"call_reasons": call_reasons}), 200


