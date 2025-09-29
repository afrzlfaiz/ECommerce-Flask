from flask import Blueprint, jsonify, request, session
from ..utils.security import require_auth
from ..services.cart_svc import get_cart, upsert_cart_item, update_quantity, delete_item

bp = Blueprint("cart", __name__)

@bp.get("")
@require_auth
def list_cart():
    uid = session["user_id"]
    data = get_cart(uid)
    return jsonify({"success": True, "items": data, "error": None}), 200

@bp.post("")
@require_auth
def add_cart():
    body = request.get_json() or {}
    pid = body.get("product_id")
    qty = int(body.get("quantity", 1))
    if not pid or qty <= 0:
        return jsonify({"success": False, "data": None, "error": {"code": "VALIDATION_ERROR", "message": "product_id and positive quantity required"}}), 422
    uid = session["user_id"]
    data = upsert_cart_item(uid, pid, qty)
    return jsonify({"success": True, "data": data, "error": None}), 201

@bp.put("/<product_id>")
@require_auth
def update_cart(product_id):
    body = request.get_json() or {}
    qty = int(body.get("quantity", 1))
    if qty <= 0:
        return jsonify({"success": False, "data": None, "error": {"code": "VALIDATION_ERROR", "message": "quantity must be > 0"}}), 422
    uid = session["user_id"]
    data = update_quantity(uid, product_id, qty)
    return jsonify({"success": True, "data": data, "error": None}), 200

@bp.delete("/<product_id>")
@require_auth
def delete_cart(product_id):
    uid = session["user_id"]
    data = delete_item(uid, product_id)
    return jsonify({"success": True, "data": data, "error": None}), 200
