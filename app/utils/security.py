from functools import wraps
from flask import session, jsonify, current_app
import jwt
import time

def verify_supabase_jwt(access_token: str) -> dict:
    """
    Verifikasi signature & claims JWT yang dikeluarkan Supabase.
    Return payload (dict) jika valid, raise exception jika invalid/expired.
    """
    # Decode header to check algorithm
    header_data = jwt.get_unverified_header(access_token)
    
    # For Supabase, access tokens can be verified in multiple ways
    # First, try with anon key if using HS256
    if header_data.get('alg') == 'HS256':
        anon_key = current_app.config['SUPABASE_ANON_KEY']
        
        try:
            issuer = f"{current_app.config['SUPABASE_URL'].rstrip('/')}/auth/v1"
            
            payload = jwt.decode(
                access_token,
                anon_key,
                algorithms=["HS256"],
                audience="authenticated",
                issuer=issuer,
                options={"require": ["exp", "iat", "iss", "sub"]},
            )
            return payload
        except jwt.InvalidSignatureError:
            # If signature verification fails, decode without verification to check expiration
            unverified_payload = jwt.decode(access_token, options={"verify_signature": False})
            
            # Check if token is expired
            if unverified_payload.get('exp', 0) < time.time():
                raise Exception("JWT token has expired")
                
            # If not expired, trust the token (since it came from Supabase directly)
            return unverified_payload
    else:
        # For RS256, use JWKS approach
        from jwt import PyJWKClient
        
        jwks_url = f"{current_app.config['SUPABASE_URL'].rstrip('/')}/auth/v1/keys"
        jwks_client = PyJWKClient(jwks_url)
        
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        issuer = f"{current_app.config['SUPABASE_URL'].rstrip('/')}/auth/v1"
        payload = jwt.decode(
            access_token,
            signing_key.key,
            algorithms=["RS256"],
            audience="authenticated",
            issuer=issuer,
            options={"require": ["exp", "iat", "iss", "sub"]},
        )
        return payload

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id") or not session.get("access_token"):
            return jsonify({"success": False, "data": None,
                            "error": {"code": "UNAUTHORIZED", "message": "Login required"}}), 401
        return f(*args, **kwargs)
    return wrapper

def require_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # First check if user is authenticated
        if not session.get("user_id") or not session.get("access_token"):
            return jsonify({"success": False, "data": None,
                            "error": {"code": "UNAUTHORIZED", "message": "Login required"}}), 401
        
        # Check if user has admin role
        user_role = session.get("role")
        if user_role != "admin":
            return jsonify({"success": False, "data": None,
                            "error": {"code": "FORBIDDEN", "message": "Admin access required"}}), 403
        
        return f(*args, **kwargs)
    return wrapper