from flask import Blueprint
from .main import bp as main_bp
from .products import bp as products_bp
from .cart import bp as cart_bp
from .orders import bp as orders_bp
from .auth import bp as auth_bp
from .admin import bp as admin_bp
from .address import bp as address_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)  # Main HTML routes
    app.register_blueprint(products_bp, url_prefix="/api/products")
    app.register_blueprint(cart_bp, url_prefix="/api/cart")
    app.register_blueprint(orders_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(address_bp, url_prefix="/api/address")
