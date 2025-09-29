from ..extensions import supabase_client
from supabase import create_client
import os

def list_orders(user_id: str):
    sb = supabase_client()
    
    # Get all orders for the user
    orders = sb.table("orders").select("*").eq("user_id", user_id).order("created_at", desc=True).execute().data
    
    # Get items for each order
    for order in orders:
        order_items = (
            sb.table("order_items")
            .select("*, product_id(name, brand, images, category)")
            .eq("order_id", order["order_id"])
            .execute()
            .data
        )
        order["items"] = order_items
    
    return orders

def get_order(user_id: str, order_id: str):
    sb = supabase_client()
    
    # Get the specific order
    order = sb.table("orders").select("*").eq("order_id", order_id).eq("user_id", user_id).single().execute().data
    
    if order:
        # Get items for this order
        order_items = (
            sb.table("order_items")
            .select("*, product_id(name, brand, images, category)")
            .eq("order_id", order_id)
            .execute()
            .data
        )
        order["items"] = order_items
    
    return order

def admin_update_status(order_id: str, status: str):
    return supabase_client().table("orders").update({"status": status}).eq("order_id", order_id).execute().data

def update_order_status(order_id: str, status: str):
    """Update order status - used for webhook updates"""
    try:
        # Untuk webhook, kita perlu menggunakan service role key agar bisa mengupdate
        # meskipun RLS membatasi update untuk non-admin
        service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        if not service_role_key:
            print("❌ Service role key not found, cannot update order status from webhook")
            return None
            
        # Buat client dengan service role key
        service_client = create_client(os.getenv("SUPABASE_URL"), service_role_key)
        
        # Cek dulu apakah order ada sebelum mencoba update
        existing_order = service_client.table("orders").select("*").eq("order_id", order_id).execute().data
        print(f"🔍 Order {order_id} found in DB before update (using service role): {len(existing_order) if existing_order else 0} records")
        
        if existing_order:
            print(f"🔍 Order {order_id} current status: {existing_order[0].get('status', 'unknown')}")
        
        # Lakukan update menggunakan service client
        result = service_client.table("orders").update({"status": status}).eq("order_id", order_id).execute()
        rows_affected = len(result.data) if result.data else 0
        
        print(f"✅ Order {order_id} status update attempt to '{status}' (using service role). Rows affected: {rows_affected}")
        
        if rows_affected == 0:
            # Jika update gagal, coba cari apakah ada perbedaan case atau masalah karakter
            print(f"❌ Update failed for order {order_id}. Checking for similar IDs...")
            
            # Ambil beberapa order terbaru untuk perbandingan
            recent_orders = service_client.table("orders").select("order_id").order("created_at", desc=True).limit(5).execute().data
            print(f"🔍 Recent order IDs in DB (using service role): {recent_orders}")
        
        return result.data
    except Exception as e:
        print(f"❌ Error updating order {order_id} status to '{status}': {str(e)}")
        import traceback
        traceback.print_exc()  # Tambahkan traceback lengkap
        raise e

def compute_cart_total(user_id: str):
    sb = supabase_client()
    items = sb.table("cart").select("*").eq("user_id", user_id).execute().data
    total = 0.0
    for it in items:
        prod = sb.table("products").select("price").eq("id", it["product_id"]).single().execute().data
        price = float(prod["price"]) if prod else 0.0
        total += price * int(it["quantity"])
    return total, items

def compute_selected_cart_total(user_id: str, product_ids: list):
    sb = supabase_client()
    items = sb.table("cart").select("*").eq("user_id", user_id).in_("product_id", product_ids).execute().data
    total = 0.0
    for it in items:
        prod = sb.table("products").select("price").eq("id", it["product_id"]).single().execute().data
        price = float(prod["price"]) if prod else 0.0
        total += price * int(it["quantity"])
    return total, items

def create_order_and_clear_cart(user_id: str, total: float, address_id: str = None):
    sb = supabase_client()
    
    # Get items from cart before clearing
    cart_items = sb.table("cart").select("*").eq("user_id", user_id).execute().data
    if not cart_items:
        return None
    
    # Get product details for each cart item
    order_items = []
    for item in cart_items:
        product = sb.table("products").select("price").eq("id", item["product_id"]).single().execute().data
        if product:
            order_item = {
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "price": product["price"]
            }
            order_items.append(order_item)
    
    # Create the order
    order_data = {"user_id": user_id, "total_price": total, "status": "pending"}  # Changed to "pending"
    if address_id:
        order_data["address_id"] = address_id
    result = sb.table("orders").insert(order_data).execute()
    order = result.data[0]  # Supabase insert always returns a list in the data field
    
    # Log the created order ID for debugging
    print(f"🔍 Created order with ID: {order['order_id']}")
    
    # Add order items to order_items table
    for item in order_items:
        sb.table("order_items").insert({
            "order_id": order["order_id"],
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "price": item["price"]
        }).execute()
    
    # Clear the cart
    sb.table("cart").delete().eq("user_id", user_id).execute()
    
    return order

def create_order_and_clear_selected_cart(user_id: str, total: float, product_ids: list, address_id: str = None):
    sb = supabase_client()
    
    # Get selected items from cart before clearing
    cart_items = sb.table("cart").select("*").eq("user_id", user_id).in_("product_id", product_ids).execute().data
    if not cart_items:
        return None
    
    # Get product details for each cart item
    order_items = []
    for item in cart_items:
        product = sb.table("products").select("price").eq("id", item["product_id"]).single().execute().data
        if product:
            order_item = {
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "price": product["price"]
            }
            order_items.append(order_item)
    
    # Create the order
    order_data = {"user_id": user_id, "total_price": total, "status": "pending"}  # Changed to "pending"
    if address_id:
        order_data["address_id"] = address_id
    result = sb.table("orders").insert(order_data).execute()
    order = result.data[0]  # Supabase insert always returns a list in the data field
    
    # Log the created order ID for debugging
    print(f"🔍 Created order with ID: {order['order_id']}")
    
    # Add order items to order_items table
    for item in order_items:
        sb.table("order_items").insert({
            "order_id": order["order_id"],
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "price": item["price"]
        }).execute()
    
    # Clear only the selected items from cart
    sb.table("cart").delete().eq("user_id", user_id).in_("product_id", product_ids).execute()
    
    return order
