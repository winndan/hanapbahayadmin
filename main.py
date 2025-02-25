from fasthtml.common import *
from monsterui.all import *
from dashboard.admin import admin_dash
from homepage.homepage import homepage
from dashboard.tabs.overview import OverviewTab
from dashboard.tabs.book import BookTab
from dashboard.forms.bookings import submit_booking
from dashboard.forms.rooms import submit_rooms
from dashboard.tabs.room import RoomTab
from dashboard.tabs.payment import PaymentTab




app, rt = fast_app(hdrs=Theme.slate.headers(daisy=True), live=True)


# Frontend

@rt("/")
async def get_homepage():
    return homepage()


@rt("/admin")
async def admin_page():
    return admin_dash()
 
@rt("/tabs/overview")
async def overview():
    return OverviewTab()

@rt("/tabs/book")
async def books():
    return BookTab()

@rt("/tabs/room")
async def rooms():
    return RoomTab()

@rt("/tabs/payment")
async def payment():
    return PaymentTab()

# backend

@rt("/submit_booking", methods=["POST"])
async def submitBook(req):
    return await submit_booking(req)

@rt("/submit_room", methods=["POST"])
async def submitRoom(req):
    return await submit_rooms(req)


if __name__ == "__main__":
    serve()
