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

# Initialize FastHTML app
app, rt = fast_app(hdrs=Theme.slate.headers(daisy=True), live=True)
@rt("/")
def room_Table():
    # Fetch all records (remove `.limit(5)`)
    response = (
        supabase.table("rooms")
        .select("room_number, room_type, description, max_guests, status, price_per_night, created_at")
        .execute()  # No limit, fetch all records
    )
    
    if not response.data:
        return P("No data found", cls="text-gray-500")

    header_data = list(response.data[0].keys()) + ["Actions"]  # Add "Actions" column
    body_data = response.data  # Show all records

    def format_date(date_str):
        """Convert Supabase timestamp to a readable format with date & time."""
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            try:
                parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                return date_str  
        return parsed_date.strftime("%b %d, %Y - %I:%M %p")  

    def body_render(k, v, row):
        """Render each column with appropriate formatting."""
        if k == "room_number":
            return Td(v, cls='font-bold')
        elif k == "price_per_night":
            return Td(f"₱{v:,.2f}")  # Format price as Peso (₱)
        elif k == "created_at":
            return Td(format_date(v), cls="text-blue-600")  # Date formatting
        return Td(v)  # Default rendering for other fields

    def row_render(row):
        """Render each row, including the delete button in a separate column."""
        return Tr(
            *[body_render(k, row[k], row) for k in row.keys()],
            Td(
                Button("Delete", cls=ButtonT.destructive, 
                    hx_delete=f"/delete/{row['room_number']}",
                    hx_confirm="Are you sure you want to delete this room?",
                    hx_target="closest tr",
                    hx_swap="outerHTML"
                )
            )  # Add delete button in a separate column
        )

    return Table(
        Thead(
            Tr(*[Th(h.upper(), cls="bg-gray-200 p-2") for h in header_data])  # Table headers
        ),
        Tbody(
            *[row_render(row) for row in body_data]  # Generate table rows dynamically
        ),
        cls="table-auto w-full border-collapse border border-gray-300"
    )



@rt("/delete/{room_number}")
def delete(room_number: int):
    """Handle DELETE request for a room."""
    try:
        response = supabase.table("rooms").delete().eq("room_number", room_number).execute()

        # If successful, return an empty response to remove the row
        return "" if response.data else Alert("Failed to delete record.", cls=AlertT.error)

    except Exception as e:
        # Catch any Supabase errors and display them
        return Alert(f"Error: {str(e)}", cls=AlertT.error)



serve()
