from flask import Blueprint, jsonify, request, session
from ..extensions import supabase_client
from ..utils.security import require_auth

bp = Blueprint("address", __name__)

@bp.get("")
@require_auth
def list_addresses():
    uid = session["user_id"]
    sb = supabase_client()
    res = sb.table("addresses").select("*").eq("user_id", uid).order("is_default", desc=True).execute()
    return jsonify({"success": True, "data": res.data})

@bp.post("")
@require_auth
def add_address():
    uid = session["user_id"]
    body = request.get_json() or {}
    body["user_id"] = uid
    sb = supabase_client()
    
    # If this is a default address, unset other default addresses for this user
    if body.get("is_default", False):
        sb.table("addresses").update({"is_default": False}).eq("user_id", uid).eq("is_default", True).execute()
    
    res = sb.table("addresses").insert(body).execute()
    return jsonify({"success": True, "data": res.data})

@bp.put("/<address_id>")
@require_auth
def update_address(address_id):
    uid = session["user_id"]
    body = request.get_json() or {}
    sb = supabase_client()
    
    # Check if address belongs to user
    addr = sb.table("addresses").select("*").eq("id", address_id).eq("user_id", uid).execute().data
    if not addr:
        return jsonify({"success": False, "error": "Address not found"}), 404
    
    # If this is being set as default, unset other default addresses for this user
    if body.get("is_default", False):
        sb.table("addresses").update({"is_default": False}).eq("user_id", uid).eq("is_default", True).execute()
    
    res = sb.table("addresses").update(body).eq("id", address_id).execute()
    return jsonify({"success": True, "data": res.data})

@bp.delete("/<address_id>")
@require_auth
def delete_address(address_id):
    uid = session["user_id"]
    sb = supabase_client()
    
    # Check if address belongs to user
    addr = sb.table("addresses").select("*").eq("id", address_id).eq("user_id", uid).execute().data
    if not addr:
        return jsonify({"success": False, "error": "Address not found"}), 404
    
    res = sb.table("addresses").delete().eq("id", address_id).execute()
    return jsonify({"success": True, "data": res.data})

@bp.get("/default")
@require_auth
def get_default_address():
    uid = session["user_id"]
    sb = supabase_client()
    res = sb.table("addresses").select("*").eq("user_id", uid).eq("is_default", True).limit(1).execute()
    if res.data:
        return jsonify({"success": True, "data": res.data[0]})
    else:
        return jsonify({"success": True, "data": None})