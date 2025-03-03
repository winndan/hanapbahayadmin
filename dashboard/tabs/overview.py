from fasthtml.common import *
import fasthtml.common as fh
from monsterui.all import *
from fasthtml.svg import *
from db_connection import supabase
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse



def InfoCard(title, value, change):
    return Card(H3(value), P(change, cls=TextPresets.muted_sm), header=H4(title))

def fetch_total_revenue():
    response = (
        supabase.table("bookings")
        .select("total_price")
        .eq("status", "Completed")
        .execute()
    )
    total_revenue = sum(item.get("total_price", 0) for item in response.data or [])
    return total_revenue

def fetch_last_month_revenue():
    today = datetime.now()
    first_day_this_month = today.replace(day=1)
    first_day_last_month = (first_day_this_month - timedelta(days=1)).replace(day=1)

    response = (
        supabase.table("bookings")
        .select("total_price")
        .eq("status", "Completed")
        .gte("created_at", first_day_last_month.isoformat())
        .lt("created_at", first_day_this_month.isoformat())
        .execute()
    )
    last_month_revenue = sum(item.get("total_price", 0) for item in response.data or [])
    return last_month_revenue

def fetch_confirmed_bookings_this_week():
    today = datetime.now(timezone.utc)
    start_of_week = today - timedelta(days=today.weekday())  # Monday as start

    response = (
        supabase.table("bookings")
        .select("id")
        .eq("status", "Confirmed")
        .gte("created_at", start_of_week.isoformat())
        .execute()
    )
    return len(response.data or [])

def fetch_ecash_subscriptions():
    response = (
        supabase.table("bookings")
        .select("id")
        .eq("payment_method", "eCash")
        .eq("status", "Confirmed")
        .execute()
    )
    return len(response.data or [])

def fetch_last_month_ecash():
    today = datetime.now()
    first_day_this_month = today.replace(day=1)
    first_day_last_month = (first_day_this_month - timedelta(days=1)).replace(day=1)

    response = (
        supabase.table("bookings")
        .select("id")
        .eq("payment_method", "eCash")
        .eq("status", "Completed")
        .gte("created_at", first_day_last_month.isoformat())
        .lt("created_at", first_day_this_month.isoformat())
        .execute()
    )
    return len(response.data or [])

def fetch_average_bookings_per_month():
    response = (
        supabase.table("bookings")
        .select("id, created_at")
        .execute()
    )
    if not response.data:
        return 0
    
    timestamps = [parse(item["created_at"]) for item in response.data if "created_at" in item]
    if not timestamps:
        return 0
    
    first_booking = min(timestamps)
    months_active = max(1, (datetime.now() - first_booking).days // 30)
    return len(timestamps) // months_active

def calculate_percentage_change(current, previous):
    if previous == 0:
        return "N/A"
    change = ((current - previous) / previous) * 100
    return f"{change:+.1f}% from last month"

total_revenue = fetch_total_revenue()
last_month_revenue = fetch_last_month_revenue()
percentage_change = calculate_percentage_change(total_revenue, last_month_revenue)
confirmed_bookings_this_week = fetch_confirmed_bookings_this_week()
ecash_subscriptions = fetch_ecash_subscriptions()
last_month_ecash = fetch_last_month_ecash()
ecash_percentage_change = calculate_percentage_change(ecash_subscriptions, last_month_ecash)
average_bookings_per_month = fetch_average_bookings_per_month()

info_card_data = [
    ("Total Revenue", f"P{total_revenue:,.2f}", percentage_change),
    ("Ecash Payment", f"+{ecash_subscriptions}", f"{ecash_percentage_change} from last month"),
    ("Sales", f"+{average_bookings_per_month}", "Average bookings per month"),
    ("Confirmed This Day", f"{confirmed_bookings_this_week}", "Bookings confirmed this week")
]

top_info_row = Grid(*[InfoCard(*row) for row in info_card_data])

def fetch_recent_bookings():
    response = (
        supabase.table("bookings")
        .select("id, guest_name, room_number, total_price, status")
        .order("created_at", desc=True)
        .limit(10)
        .execute()
    )
    return response.data or []

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

def OverviewTab():
    return Div(
        H2("Dashboard Overview"),
        top_info_row,
        RecentBookingsTable()
    )


