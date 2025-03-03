from fasthtml.common import *
from db_connection import supabase

def login_admin(email: str, password: str):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})

        if not response or not hasattr(response, "session") or not response.session:
            return {"status": "error", "message": "Invalid credentials"}

        access_token = response.session.access_token  # ✅ Get actual JWT token

        # ✅ Check if user is an admin
        user_id = response.user.id
        role_check = supabase.table("roles").select("name").eq("user_id", user_id).single().execute()
        
        if role_check and role_check.data and role_check.data.get("name") == "admin":
            return {"status": "success", "access_token": access_token}  # ✅ Return correct token
        else:
            return {"status": "error", "message": "Access denied: User is not an admin."}

    except Exception as e:
        print(f"🚨 Login error: {e}")
        return {"status": "error", "message": f"Login error: {e}"}
