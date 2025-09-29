from ..extensions import supabase_client

def signup(email, password):
    sb = supabase_client()
    # Include redirect URL for email confirmation
    result = sb.auth.sign_up({"email": email, "password": password})
    return result

def login(email, password):
    sb = supabase_client()
    result = sb.auth.sign_in_with_password({"email": email, "password": password})
    return result

def logout():
    sb = supabase_client()
    return sb.auth.sign_out()

def reset_password(email, redirect_to=None):
    sb = supabase_client()
    options = {"email_redirect_to": redirect_to} if redirect_to else {}
    return sb.auth.reset_password_for_email(email, options)
