from flask import Blueprint, jsonify, session, request, redirect, url_for
from ..extensions import supabase_client
from ..utils.security import require_auth
from ..services.orders_svc import list_orders, get_order, compute_cart_total, create_order_and_clear_cart, compute_selected_cart_total, create_order_and_clear_selected_cart, update_order_status
import os
import requests
from urllib.parse import urljoin

bp = Blueprint("orders", __name__)

@bp.post("/checkout")
@require_auth
def checkout():
    uid = session["user_id"]
    print(f"Checkout request for user: {uid}")  # Debug log
    body = request.get_json() or {}
    selected_product_ids = body.get("product_ids")  # Optional: array of product IDs to checkout
    address_id = body.get("address_id")  # Required: address ID for shipping
    
    print(f"Selected product IDs: {selected_product_ids}")  # Debug log
    print(f"Address ID: {address_id}")  # Debug log
    
    # Validate address
    if not address_id:
        # Try to get default address if no address_id provided
        sb = supabase_client()
        addr = sb.table("addresses").select("id").eq("user_id", uid).eq("is_default", True).limit(1).execute().data
        if addr:
            address_id = addr[0]["id"]
        else:
            return jsonify({"success": False, "data": None, "error": {"code": "ADDRESS_REQUIRED", "message": "Shipping address required"}}, 400)
    
    # Validate address belongs to user
    sb = supabase_client()
    addr = sb.table("addresses").select("*").eq("id", address_id).eq("user_id", uid).execute().data
    if not addr:
        return jsonify({"success": False, "data": None, "error": {"code": "INVALID_ADDRESS", "message": "Invalid shipping address"}}, 400)

    if selected_product_ids and isinstance(selected_product_ids, list) and len(selected_product_ids) > 0:
        # Checkout only selected products
        print(f"Checking out selected products: {selected_product_ids}")  # Debug log
        total, items = compute_selected_cart_total(uid, selected_product_ids)
        if not items:
            return jsonify({"success": False, "data": None, "error": {"code": "EMPTY_CART", "message": "No selected items in cart"}}, 400)
        
        order = create_order_and_clear_selected_cart(uid, total, selected_product_ids, address_id)
        print(f"Created order for selected items: {order}")  # Debug log
    else:
        # Checkout all products
        print("Checking out all products")  # Debug log
        total, items = compute_cart_total(uid)
        if not items:
            return jsonify({"success": False, "data": None, "error": {"code": "EMPTY_CART", "message": "No items in cart"}}, 400)
        
        order = create_order_and_clear_cart(uid, total, address_id)
        print(f"Created order for all items: {order}")  # Debug log
    
    return jsonify({"success": True, "data": {"order": order, "total": total}, "error": None}), 201

@bp.get("/orders")
@require_auth
def my_orders():
    uid = session["user_id"]
    print(f"Fetching orders for user: {uid}")  # Debug log
    data = list_orders(uid)
    print(f"Found {len(data) if data else 0} orders")  # Debug log
    return jsonify({"success": True, "data": data, "error": None}), 200

@bp.get("/orders/<order_id>")
@require_auth
def order_detail(order_id):
    uid = session["user_id"]
    data = get_order(uid, order_id)
    if not data:
        return jsonify({"success": False, "data": None, "error": {"code": "NOT_FOUND", "message": "Order not found"}}), 404
    return jsonify({"success": True, "data": data, "error": None}), 200

# Route untuk redirect ke Xendit pembayaran
@bp.get("/pay/<order_id>")
@require_auth
def pay_order(order_id):
    try:
        # Ambil data order dari Supabase
        order = supabase_client().table("orders").select("*").eq("order_id", order_id).single().execute().data
        
        # Verifikasi bahwa order milik user saat ini
        if order["user_id"] != session["user_id"]:
            return jsonify({"success": False, "data": None, "error": {"code": "FORBIDDEN", "message": "Access denied"}}, 403)
        
        user_email = session.get("user_email")  # Email mungkin disimpan di session saat login
        
        # Ambil email dari data pengguna jika tidak ada di session
        if not user_email:
            user_data = supabase_client().auth.get_user(session.get("access_token"))
            user_email = user_data.user.email
        
        # Ambil XENDIT_SECRET_KEY dari environment
        xendit_secret_key = os.getenv("XENDIT_SECRET_KEY")
        if not xendit_secret_key:
            return jsonify({"success": False, "data": None, "error": {"code": "CONFIG_ERROR", "message": "Xendit configuration not found"}}, 500)
        
        # Log order info for debugging
        print(f"🔍 Preparing Xendit invoice for order: {order_id}, amount: {order['total_price']}")
        
        # Buat payload untuk invoice Xendit
        payload = {
            "external_id": order_id,
            "amount": float(order["total_price"]),
            "payer_email": user_email,
            "description": f"Pembayaran untuk pesanan {order_id}",
            "success_redirect_url": url_for("main.order_detail_page", order_id=order_id, _external=True) + "?from_payment=true",
            "failure_redirect_url": url_for("main.order_detail_page", order_id=order_id, _external=True)
        }

        # Buat invoice di Xendit
        resp = requests.post(
            "https://api.xendit.co/v2/invoices",
            json=payload,
            auth=(xendit_secret_key, "")
        )
        
        if resp.status_code != 200:
            print(f"Error creating Xendit invoice: {resp.text}")
            return jsonify({"success": False, "data": None, "error": {"code": "XENDIT_ERROR", "message": resp.text}}, 500)
        
        invoice = resp.json()

        # Redirect user ke halaman pembayaran Xendit
        return redirect(invoice["invoice_url"])
    except Exception as e:
        print(f"Error in pay_order: {str(e)}")
        return jsonify({"success": False, "data": None, "error": {"code": "PAYMENT_ERROR", "message": str(e)}}, 500)

# Webhook untuk menerima callback dari Xendit
@bp.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Tambahkan logging untuk debugging
        print(f"Webhook received at {request.url}")
        print(f"Request headers: {dict(request.headers)}")
        
        data = request.get_json()
        print(f"Request data: {data}")
        
        # Verifikasi webhook token jika disediakan
        x_callback_token = request.headers.get("x-callback-token")
        webhook_token = os.getenv("WEBHOOK_TOKEN")
        
        # Jika webhook token diatur di environment, lakukan verifikasi
        if webhook_token:
            if not x_callback_token or x_callback_token != webhook_token:
                print(f"Webhook token mismatch. Expected: {webhook_token}, Received: {x_callback_token}")
                return jsonify({"message": "Unauthorized"}), 401

        status = data.get("status")
        order_id = data.get("external_id")

        if status == "PAID":
            # Update status order menjadi 'paid'
            update_order_status(order_id, "paid")
            print(f"✅ Pembayaran untuk order {order_id} berhasil!")
            
        elif status == "EXPIRED":
            # Update status order menjadi 'expired' atau tetap 'pending'
            update_order_status(order_id, "pending")
            print(f"⚠️ Pembayaran untuk order {order_id} kadaluarsa.")
            
        elif status == "FAILED":
            # Update status order menjadi 'failed' atau tetap 'pending'
            update_order_status(order_id, "pending")
            print(f"❌ Pembayaran untuk order {order_id} gagal.")

        return jsonify({"message": "Webhook received"}), 200
    except Exception as e:
        print(f"Error processing webhook: {e}")
        import traceback
        traceback.print_exc()  # Tambahkan traceback untuk debugging
        return jsonify({"message": "Error processing webhook"}), 500
