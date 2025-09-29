from flask import Blueprint, request, jsonify
from ..utils.security import require_admin
from ..services.orders_svc import admin_update_status

bp = Blueprint("admin", __name__)

@bp.patch("/orders/<order_id>/status")
@require_admin
def update_status(order_id):
    body = request.get_json() or {}
    status = body.get("status")
    if status not in ("paid","delivered"):
        return jsonify({"success": False, "data": None, "error": {"code": "VALIDATION_ERROR", "message": "status must be 'paid' or 'delivered'"}}), 422
    data = admin_update_status(order_id, status)
    return jsonify({"success": True, "data": data, "error": None}), 200
