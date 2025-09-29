from ..extensions import supabase_client

def get_cart(user_id: str):
    sb = supabase_client()
    cart_items = sb.table("cart").select("*").eq("user_id", user_id).execute().data

    if not cart_items:
        return []

    product_ids = [c["product_id"] for c in cart_items]
    products = sb.table("products").select("id,name,price,brand,images").in_("id", product_ids).execute().data

    product_map = {p["id"]: p for p in products}

    # Gabungkan data cart + produk
    result = []
    for c in cart_items:
        p = product_map.get(c["product_id"])
        if p:
            merged = {**c, **p}
            result.append(merged)
    return result

def upsert_cart_item(user_id: str, product_id: str, quantity: int):
    # Try update first
    sb = supabase_client()
    existing = sb.table("cart").select("cart_id,quantity").eq("user_id", user_id).eq("product_id", product_id).execute().data
    if existing:
        return sb.table("cart").update({"quantity": quantity}).eq("user_id", user_id).eq("product_id", product_id).execute().data
    return sb.table("cart").insert({"user_id": user_id, "product_id": product_id, "quantity": quantity}).execute().data

def update_quantity(user_id: str, product_id: str, quantity: int):
    return supabase_client().table("cart").update({"quantity": quantity}).eq("user_id", user_id).eq("product_id", product_id).execute().data

def delete_item(user_id: str, product_id: str):
    return supabase_client().table("cart").delete().eq("user_id", user_id).eq("product_id", product_id).execute().data
