from fasthtml.common import *
import fasthtml.common as fh
from monsterui.all import *
from fasthtml.svg import *
from db_connection import supabase

# Initialize FastHTML App
app, rt = fast_app(hdrs=Theme.blue.headers())

def InfoCard(title, value, change):
    return Card(H3(value), P(change, cls=TextPresets.muted_sm), header=H4(title))

info_card_data = [
    ("Total Revenue", "$45,231.89", "+20.1% from last month"),
    ("Subscriptions", "+2,350", "+180.1% from last month"),
    ("Sales", "+12,234", "+19% from last month"),
    ("Active Now", "+573", "+201 since last hour")
]

top_info_row = Grid(*[InfoCard(*row) for row in info_card_data])

def fetch_recent_bookings():
    response = (
        supabase.table("bookings")
        .select("id, guest_name, room_number, total_price, status")
        .order("created_at", desc=True)
        .limit(10)  # Updated to fetch 10 records
        .execute()
    )
    return response.data if response.data else []

def BookingItem(guest, room, price, status):
    return DivFullySpaced(
        DivLAligned(
            DiceBearAvatar(guest, 9, 9),
            Div(
                Strong(guest, cls=TextT.sm),
                P(f"Room {room} - {status}", cls=TextPresets.muted_sm),
            ),
        ),
        fh.Data(f"${price:.2f}", cls="ml-auto font-medium", value=str(price))
    )

def RecentBookingsTable():
    bookings = fetch_recent_bookings()
    
    return Card(
        Div(cls="space-y-6")(
            *[BookingItem(b["guest_name"], b["room_number"], b["total_price"], b["status"]) for b in bookings]
        ),
        header=Div(H3("Recent Bookings"), Subtitle("Latest room bookings.")),
        cls='col-span-3'
    )

@rt("/")
def OverviewTab():
    return Div(
        H2("Dashboard Overview"),
        top_info_row,
        RecentBookingsTable()
    )

serve()
