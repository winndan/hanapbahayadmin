from fasthtml.common import *
from monsterui.all import *
from dashboard.admin import admin_dash
from homepage.homepage import homepage
from dashboard.forms.bookings import submit_booking
from dashboard.forms.rooms import submit_rooms

app, rt = fast_app(hdrs=Theme.slate.headers(daisy=True), live=True)

# ✅ Frontend
@rt("/")
async def get_homepage():
    return homepage()

@rt("/admin")
async def admin_page(req):
    tab = req.query_params.get("tab", "overview")  # ✅ Extract active tab
    return admin_dash(tab)  # ✅ Pass the active tab

# ✅ Backend
@rt("/submit_booking", methods=["POST"])
async def submitBook(req):
    return await submit_booking(req)

@rt("/submit_room", methods=["POST"])
async def submitRoom(req):
    return await submit_rooms(req)

if __name__ == "__main__":
    serve()
