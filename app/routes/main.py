from flask import Blueprint, render_template, request, jsonify
from ..services.products_svc import list_products, get_product
from ..utils.validators import parse_int, parse_float

bp = Blueprint("main", __name__)

@bp.route("/")
@bp.route("/home")
def home():
    brand = request.args.get("brand")
    category = request.args.get("category")
    min_price = parse_float(request.args.get("min_price"))
    max_price = parse_float(request.args.get("max_price"))
    min_rating = parse_float(request.args.get("min_rating"))
    sort = request.args.get("sort", "created_desc")
    page = parse_int(request.args.get("page"), 1, 1)
    limit = parse_int(request.args.get("limit"), 20, 1, 100)

    # Get products for the grid
    try:
        products_data = list_products(
            {"brand": brand, "category": category, "min_price": min_price, "max_price": max_price, "min_rating": min_rating},
            page, limit, sort
        )
    except Exception as e:
        # Log the error but continue with empty data
        print(f"Error fetching products: {e}")
        products_data = {"items": [], "page": 1, "has_more": False, "page_size": 20}
    
    return render_template("home.html", products=products_data)

@bp.route("/products")
def products():
    return render_template("products.html")

@bp.route("/products/<prod_id>")
def product_detail(prod_id):
    # Get the product data to pass to the template
    print(f"Fetching product with ID: {prod_id}")  # Debug log
    product_data = get_product(prod_id)
    print(f"Product data: {product_data}")  # Debug log
    if not product_data:
        # If product not found, we can still render the template and let JS handle the error
        print(f"Product with ID {prod_id} not found")  # Debug log
        return render_template("detail.html", product_id=prod_id)
    return render_template("detail.html", product_id=prod_id, product=product_data)

@bp.route("/cart")
def cart():
    return render_template("cart.html")

@bp.route("/checkout")
def checkout():
    return render_template("checkout.html")

@bp.route("/orders")
def orders():
    return render_template("orders.html")

@bp.route("/orders/<order_id>")
def order_detail_page(order_id):
    # Halaman detail order - ini hanya untuk menampilkan template
    # Data order akan diambil melalui API oleh JavaScript
    return render_template("orders.html", order_id=order_id)

@bp.route("/login")
def login():
    return render_template("login.html")

@bp.route("/register")
def register():
    return render_template("register.html")

@bp.route("/auth/callback")
def auth_callback():
    # Halaman tipis; proses OAuth dikerjakan di browser (supabase-js)
    return render_template("auth_callback.html")