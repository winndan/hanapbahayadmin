from fasthtml.common import *
from monsterui.all import *
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from uuid import UUID, uuid4
from datetime import datetime

# Load environment variables
load_dotenv()

url: str = os.getenv('supa_url')
key: str = os.getenv('supa_key')

supabase: Client = create_client(url, key)

app, rt = fast_app(hdrs=Theme.slate.headers(daisy=True), live=True)

@rt("/")
def booking_table():
    """Fetch and display the latest 10 bookings, excluding `id` from the table."""
    response = (
        supabase.table("bookings")
        .select("id, room_number, guest_name, guest_email, guest_phone, check_in_date, check_out_date, number_of_guests, total_price, status, created_at")
        .order("created_at", desc=True)  # ✅ Order by latest created_at
        .limit(10)  # ✅ Show only 10 latest records
        .execute()
    )

    if not response.data:
        return P("No recent bookings found", cls="text-gray-500")

    # ✅ Remove 'id' from displayed headers
    header_data = [key for key in response.data[0].keys() if key != "id"] + ["Actions"]

    def row_render(row):
        """Render each row without displaying the `id` column but still keeping it for updates."""
        row_id = row["id"]  # ✅ Keep ID for updates but don't show it
        return Tr(
            *[
                Td(row[k]) if k != "status" else Td(
                    Select(
                        *[Option(status, selected=(status == row[k])) for status in ["Pending", "Confirmed", "Cancelled", "Completed"]],
                        name="status",
                        cls="border rounded p-1"
                    ),
                    id=f"status-{row_id}"
                )
                for k in row.keys() if k != "id"  # ✅ Exclude 'id' from table
            ],
            Td(  # ✅ Actions Column - Only "Update" button here
                Form(
                    Input(type="hidden", name="id", value=row_id),  # ✅ Hidden input to send ID for updates
                    Button("Update", cls=ButtonT.primary,
                        hx_patch=f"/update_status/{row_id}",
                        hx_target=f"#status-{row_id}",
                        hx_include="closest tr",
                        hx_swap="outerHTML"
                    ),
                    cls="p-2"
                ),
                id=f"action-{row_id}"
            )
        )

    return Table(
        Thead(Tr(*[Th(h.upper(), cls="bg-gray-200 p-2") for h in header_data])),
        Tbody(*[row_render(row) for row in response.data]),
        cls="table-auto w-full border-collapse border border-gray-300"
    )

@rt("/update_status/{booking_id}", methods=["PATCH"])
async def update_status(booking_id: UUID, req):
    """Handle PATCH request to update booking status."""
    try:
        form_data = await req.form()
        new_status = form_data.get("status", "").strip()

        valid_statuses = ["Pending", "Confirmed", "Cancelled", "Completed"]
        if new_status not in valid_statuses:
            return Alert(f"Invalid status value: {new_status}", cls=AlertT.warning)

        booking_id_str = str(booking_id)

        response = supabase.table("bookings").update({"status": new_status}).eq("id", booking_id_str).execute()

        if response.data:
            return Div(
                Select(
                    *[Option(status, selected=(status == new_status)) for status in valid_statuses],
                    name="status",
                    cls="border rounded p-1"
                ),
                Alert("Status updated successfully!", cls=AlertT.success, id=f"alert-{booking_id}"),
                Script(f"setTimeout(() => document.getElementById('alert-{booking_id}').remove(), 3000);")  # Auto-hide after 3s
            )

        return Alert("Failed to update status.", cls=AlertT.error)

    except Exception as e:
        return Alert(f"Error: {str(e)}", cls=AlertT.error)

serve()
