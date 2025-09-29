from flask import Blueprint, request, jsonify
from ..services.products_svc import list_products, get_product, admin_upsert_product, admin_delete_product
from ..utils.validators import parse_int, parse_float
from ..utils.security import require_admin

bp = Blueprint("products", __name__)

@bp.get("")
def list_():
    brand = request.args.get("brand")
    category = request.args.get("category")
    min_price = parse_float(request.args.get("min_price"))
    max_price = parse_float(request.args.get("max_price"))
    min_rating = parse_float(request.args.get("min_rating"))
    sort = request.args.get("sort", "created_desc")
    page = parse_int(request.args.get("page"), 1, 1)
    limit = parse_int(request.args.get("limit"), 20, 1, 100)
    # For regular listing, no search query is passed

    data = list_products(
        {"brand": brand, "category": category, "min_price": min_price, "max_price": max_price, "min_rating": min_rating},
        page, limit, sort
    )
    return jsonify({"success": True, "data": data, "error": None}), 200

@bp.get("/<prod_id>")
def detail(prod_id):
    data = get_product(prod_id)
    if not data:
        return jsonify({"success": False, "data": None, "error": {"code": "NOT_FOUND", "message": "Product not found"}}, 404)
    return jsonify({"success": True, "data": data, "error": None}), 200

@bp.get("/search")
def search_products():
    search_query = request.args.get("q", "")
    brand = request.args.get("brand")
    category = request.args.get("category")
    min_price = parse_float(request.args.get("min_price"))
    max_price = parse_float(request.args.get("max_price"))
    min_rating = parse_float(request.args.get("min_rating"))
    sort = request.args.get("sort", "created_desc")
    page = parse_int(request.args.get("page"), 1, 1)
    limit = parse_int(request.args.get("limit"), 20, 1, 100)

    if not search_query:
        return jsonify({"success": False, "data": [], "error": {"code": "VALIDATION_ERROR", "message": "Query parameter 'q' is required for search"}}, 400)

    # Build filters dictionary
    filters = {"brand": brand, "category": category, "min_price": min_price, "max_price": max_price, "min_rating": min_rating}

    try:
        data = list_products(
            filters,
            page, limit, sort,
            search_query=search_query  # Pass search query to the service function
        )
        return jsonify({"success": True, "data": data, "error": None}), 200
    except Exception as e:
        print(f"Search products error: {str(e)}")  # Debug log
        return jsonify({"success": False, "data": [], "error": {"code": "SEARCH_ERROR", "message": str(e)}}), 500

@bp.post("")
@require_admin
def admin_create():
    payload = (request.get_json() or {})
    if not payload.get("id"):
        return jsonify({"success": False, "data": None, "error": {"code": "VALIDATION_ERROR", "message": "id is required"}}), 422
    data = admin_upsert_product(payload)
    return jsonify({"success": True, "data": data, "error": None}), 201

@bp.put("/<prod_id>")
@require_admin
def admin_update(prod_id):
    payload = (request.get_json() or {})
    payload["id"] = prod_id
    data = admin_upsert_product(payload)
    return jsonify({"success": True, "data": data, "error": None}), 200

@bp.delete("/<prod_id>")
@require_admin
def admin_delete(prod_id):
    data = admin_delete_product(prod_id)
    return jsonify({"success": True, "data": data, "error": None}), 200
