from flask import Flask, jsonify
from .config import Config
from .extensions import cors, supabase_client, attach_user_token
from .routes import register_blueprints
import os

def create_app():
    # Set up template and static folders relative to project root
    project_root = os.path.dirname(os.path.dirname(__file__))
    app = Flask(__name__, 
                template_folder=os.path.join(project_root, 'templates'),
                static_folder=os.path.join(project_root, 'static'))
    app.config.from_object(Config)
    
    # Get the origins list from the config property
    config_obj = Config()
    origins_list = config_obj.ALLOWED_ORIGINS_LIST

    cors.init_app(app, resources={r"/api/*": {"origins": origins_list}})

    # Session configuration
    app.config.update(
        SESSION_COOKIE_SAMESITE='Lax',  # Allow cross-site requests
        SESSION_COOKIE_HTTPONLY=True,   # Prevent XSS
        SESSION_COOKIE_SECURE=False,    # Set to True in production with HTTPS
    )

    # Before each request, if we have a user token in session, attach it to PostgREST client
    app.before_request(attach_user_token)

    @app.context_processor
    def inject_config():
        # Memungkinkan template mengakses config["SUPABASE_URL"], dll.
        return {"config": app.config}

    # Health check
    @app.get("/api/health")
    def health():
        return jsonify({"success": True, "data": {"status": "ok"}}), 200

    register_blueprints(app)
    return app
