from supabase import Client
from ..extensions import supabase_client

def list_products(filters: dict, page: int, limit: int, sort: str, search_query: str = None):
    sb = supabase_client()
    query = sb.table("products").select("*")

    # Apply search filter if search_query is provided
    if search_query:
        query = query.ilike("name", f"%{search_query}%")

    if (brand := filters.get("brand")):
        query = query.eq("brand", brand)
    if (category := filters.get("category")):
        query = query.eq("category", category)
    if (min_price := filters.get("min_price")) is not None:
        query = query.gte("price", min_price)
    if (max_price := filters.get("max_price")) is not None:
        query = query.lte("price", max_price)
    if (min_rating := filters.get("min_rating")) is not None:
        query = query.gte("rating", min_rating)

    # Sorting
    if sort == "bestseller" or sort == "sold_desc":
        query = query.order("sold_count", desc=True)
    elif sort == "rating_desc":
        query = query.order("rating", desc=True)
    elif sort == "price_asc":
        query = query.order("price", desc=False)
    elif sort == "price_desc":
        query = query.order("price", desc=True)
    else:
        query = query.order("created_at", desc=True)

    start = (page - 1) * limit
    end = start + limit - 1
    data = query.range(start, end).execute().data
    return data

def get_product(prod_id: str):
    try:
        result = supabase_client().table("products").select("*").eq("id", prod_id).single().execute()
        return result.data
    except Exception as e:
        print(f"Error getting product {prod_id}: {str(e)}")
        return None

def admin_upsert_product(payload: dict):
    # insert or update by id
    return supabase_client().table("products").upsert(payload).execute().data

def admin_delete_product(prod_id: str):
    return supabase_client().table("products").delete().eq("id", prod_id).execute().data
