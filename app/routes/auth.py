from flask import Blueprint, request, jsonify, session
from ..services.auth_svc import signup, login, logout, reset_password
from ..utils.security import verify_supabase_jwt   # <-- tambah ini

bp = Blueprint("auth", __name__)

@bp.post("/signup")
def do_signup():
    body = request.get_json() or {}
    email = body.get("email"); password = body.get("password")
    if not email or not password:
        return jsonify({"success": False, "data": None, "error": {"code": "VALIDATION_ERROR", "message": "email & password required"}}), 422
    try:
        resp = signup(email, password)
        # Extract only serializable data from response
        user_data = None
        if hasattr(resp, 'user') and resp.user:
            user_data = {
                "id": getattr(resp.user, "id", None),
                "email": getattr(resp.user, "email", None),
                "email_confirmed_at": getattr(resp.user, "email_confirmed_at", None)
            }
        return jsonify({"success": True, "data": {"user": user_data}, "error": None}), 201
    except Exception as e:
        return jsonify({"success": False, "data": None, "error": {"code": "SIGNUP_ERROR", "message": str(e)}}), 500

@bp.post("/login")
def do_login():
    body = request.get_json() or {}
    email = body.get("email"); password = body.get("password")
    if not email or not password:
        return jsonify({"success": False, "data": None, "error": {"code": "VALIDATION_ERROR", "message": "email & password required"}}, 422)
    try:
        resp = login(email, password)
        if not getattr(resp, "session", None):
            return jsonify({"success": False, "data": None, "error": {"code":"AUTH_FAILED","message":"Invalid credentials or email not confirmed"}}, 401)

        # store in session
        session["access_token"] = resp.session.access_token
        session["user_id"] = resp.user.id
        session["user_email"] = resp.user.email  # Simpan email ke session
        # Try to read role from app_metadata
        role = None
        try:
            role = (resp.user.app_metadata or {}).get("role")
        except Exception:
            pass
        session["role"] = role
        
        return jsonify({"success": True, "data": {"user_id": resp.user.id, "email": resp.user.email, "role": role}, "error": None}), 200
    except Exception as e:
        return jsonify({"success": False, "data": None, "error": {"code": "LOGIN_ERROR", "message": str(e)}}, 500)

@bp.post("/logout")
def do_logout():
    try:
        logout()
    except Exception:
        pass
    session.clear()
    return jsonify({"success": True, "data": {"message": "logged out"}, "error": None}), 200

@bp.post("/reset-password")
def do_reset():
    body = request.get_json() or {}
    email = body.get("email")
    redirect_to = body.get("redirect_to")
    if not email:
        return jsonify({"success": False, "data": None, "error": {"code": "VALIDATION_ERROR", "message": "email required"}}), 422
    reset_password(email, redirect_to)
    return jsonify({"success": True, "data": {"message": "Password reset email sent if the account exists"} , "error": None}), 200

@bp.post("/session")
def adopt_session():
    """
    Terima access_token (hasil OAuth Supabase di browser),
    verifikasi via JWKS, lalu simpan ke session Flask (cookie).
    """
    body = request.get_json() or {}
    token = body.get("access_token")
    if not token:
        return jsonify({"success": False, "data": None,
                        "error": {"code": "VALIDATION_ERROR", "message": "access_token required"}}), 422
    try:
        payload = verify_supabase_jwt(token)
    except Exception as e:
        return jsonify({"success": False, "data": None,
                        "error": {"code": "INVALID_TOKEN", "message": f"Invalid or expired Supabase token: {str(e)}"}}), 401

    session["access_token"] = token
    session["user_id"] = payload.get("sub")                # UUID user Supabase
    session["user_email"] = payload.get("email") or session.get("user_email")  # Gunakan email dari payload atau tetap simpan yang lama
    session["role"] = payload.get("role") or "authenticated"
    return jsonify({"success": True, "data": {"user_id": session["user_id"], "email": session["user_email"]}, "error": None}), 200

@bp.get("/me")
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"success": True, "data": None, "error": None}), 200
    return jsonify({"success": True, "data": {"user_id": user_id, "role": session.get("role")}, "error": None}), 200
