from flask import session, current_app
from flask_cors import CORS
from supabase import create_client, Client

cors = CORS()
_supabase: Client | None = None

def supabase_client() -> Client:
    global _supabase
    if _supabase is None:
        _supabase = create_client(current_app.config["SUPABASE_URL"], current_app.config["SUPABASE_ANON_KEY"])
    return _supabase

def attach_user_token():
    # If user is logged in, attach their access token to Postgrest so RLS uses auth.uid()
    token = session.get("access_token")
    if token:
        try:
            supabase_client().postgrest.auth(token)
        except:
            # If setting auth fails, continue without error
            pass
