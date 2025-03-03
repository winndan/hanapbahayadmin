import os
from fasthtml.common import *
from monsterui.all import *
from db_connection import supabase
from dashboard.admin import admin_dash
from dashboard.forms.rooms import submit_rooms
from dashboard.forms.bookings import submit_booking
from dashboard.table.bookings import update_status
from uuid import UUID, uuid4
from auths.frontend.signin import login_page



# 🔹 Authentication Middleware
def before(req):
    """Middleware to check if the user is authenticated before serving protected routes."""
    session = req.session  # ✅ Get session from request
    auth = req.scope['auth'] = session.get('user_id', None)
    
    if not auth:
        return Redirect("/")  # ✅ Redirect to login page
    
bware = Beforeware(before, skip=['/', '/login', '/logout', '/assets/favicon.ico','/assets/logo-bg.png'])


# ✅ Assign `before` function directly
app, rt = fast_app(hdrs=Theme.blue.headers(daisy=True), live=True, before=bware)


# 🔹 Function to authenticate users
def login_admin(email: str, password: str, session):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})

        if not response or not hasattr(response, "session") or not response.session:
            return {"status": "error", "message": "Invalid credentials"}

        # ✅ Store user session
        user_id = response.user.id
        session["user_id"] = user_id

        # ✅ Check if user is an admin
        role_check = supabase.table("roles").select("name").eq("user_id", user_id).execute()
        
        if not role_check.data or len(role_check.data) == 0:
            return {"status": "error", "message": "Access denied: No role assigned."}

        if role_check.data[0]["name"] == "admin":
            return {"status": "success"}
        else:
            return {"status": "error", "message": "Access denied: User is not an admin."}

    except Exception as e:
        print(f"🚨 Login error: {e}")
        return {"status": "error", "message": f"Login error: {e}"}

# 🔹 Login Page
@rt("/")
def index():
    return login_page()
# 🔹 Login Route
@rt("/login")
def login(req, email: str = Form(...), password: str = Form(...)):
    session = req.session  # ✅ Get session from request
    result = login_admin(email, password, session)

    if result["status"] == "success":
        return Redirect("/admin")  # ✅ Redirect to dashboard
    
    return Div(f"❌ {result['message']}", cls="text-red-500")

# ✅ Backend
@rt("/submit_booking", methods=["POST"])
async def submitBook(req):
    return await submit_booking(req)

@rt("/submit_room", methods=["POST"])
async def submitRoom(req):
    return await submit_rooms(req)

# 🔹 Protected Admin Dashboard (Only logged-in users can access)
@rt("/admin")
async def admin_page(req):
    tab = req.query_params.get("tab", "overview")  # ✅ Extract active tab
    return admin_dash(tab)  # ✅ Pass the active tab

# 🔹 Logout Route
@rt("/logout")
def logout(req):
    req.session.clear()  # ✅ Clear session
    return Redirect("/")

@rt("/delete/{room_number}", methods=["DELETE"])
def delete_room(req, room_number: int):
    """Handle DELETE request for a room."""
    try:
        response = supabase.table("rooms").delete().eq("room_number", room_number).execute()

        # If successful, return an empty response to remove the row
        return "" if response.data else Alert("Failed to delete record.", cls=AlertT.error)

    except Exception as e:
        # Catch any Supabase errors and display them
        return Alert(f"Error: {str(e)}", cls=AlertT.error)
    

@rt("/update_status/{booking_id}", methods=["PATCH"])
async def updated_status(req, booking_id: UUID):
    return await update_status(booking_id, req)

    


if __name__ == "__main__":
    serve()
