from fasthtml.common import *
from monsterui.all import *
from pydantic import BaseModel, Field, EmailStr, conint, condecimal, field_validator
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from uuid import UUID, uuid4
from datetime import date
import re  # For phone number validation
from db_connection import supabase as db

# ==============================
# 📌 Load Environment Variables
# ==============================


supabase = db

# ==============================
# 📌 Initialize FastHTML App
# ==============================

# ==============================
# 📌 Pydantic Booking Model (Updated)
# ==============================
class BookingModel(BaseModel):
    """Pydantic model for booking validation."""
    room_number: str = Field(..., min_length=1, max_length=10)  
    guest_name: str = Field(..., min_length=1, max_length=100)  
    guest_email: EmailStr  
    guest_phone: str = Field(..., min_length=10, max_length=15)  
    check_in_date: date
    check_out_date: date
    number_of_guests: conint(gt=0)  
    total_price: condecimal(gt=0, max_digits=10, decimal_places=2)  
    status: str = Field(..., pattern="^(Pending|Confirmed|Cancelled|Completed)$")  
    payment_method: str = Field(..., pattern="^(Cash|eCash)$")  
    reference_number: str | None = None  # Required if payment is eCash

    @field_validator("guest_phone", mode="before")
    @classmethod
    def validate_phone(cls, phone: str):
        """Ensure phone number is valid (basic regex for digits and + sign)."""
        if not re.match(r"^\+?[0-9\- ]{10,15}$", phone):
            raise ValueError("Invalid phone number format.")
        return phone

    @field_validator("check_out_date", mode="before")
    @classmethod
    def validate_dates(cls, check_out_date, info):
        """Ensure check-out date is after check-in date."""
        check_in_date = info.data.get("check_in_date")  
        if check_in_date and check_out_date <= check_in_date:
            raise ValueError("Check-out date must be after check-in date.")
        return check_out_date

    @field_validator("reference_number", mode="before")
    @classmethod
    def validate_reference_number(cls, reference_number, info):
        """Ensure reference number is required only for eCash payments."""
        payment_method = info.data.get("payment_method")
        if payment_method == "eCash" and not reference_number:
            raise ValueError("Reference number is required for eCash payments.")
        if payment_method == "Cash" and reference_number:
            raise ValueError("Reference number must be empty for Cash payments.")
        return reference_number

    class Config:
        from_attributes = True  


# ==============================
# 📌 Booking Form (Updated with Payment Fields)
# ==============================
def booking_form():
    """Booking form to collect guest details."""
    statuses = ["Pending", "Confirmed", "Cancelled", "Completed"]  
    payment_methods = ["Cash", "eCash"]

    return Titled("Room Booking Form",
        Form(method="post", action="/submit_booking", enctype="multipart/form-data",
             hx_post="/submit_booking", hx_target="#form-status", hx_swap="outerHTML",
             hx_on="htmx:afterRequest:this.reset()")(  
            Grid(
                LabelInput("Guest Name", name="guest_name"),
                LabelInput("Guest Email", name="guest_email", type="email"),
                LabelInput("Phone Number", name="guest_phone", type="tel"),
            ),
            Grid(
                LabelInput("Room Number", name="room_number"),  
                LabelInput("Check-in Date", name="check_in_date", type="date"),
                LabelInput("Check-out Date", name="check_out_date", type="date"),
            ),
            Grid(
                LabelInput("Number of Guests", name="number_of_guests", type="number", min="1"),
                LabelInput("Total Price (₱)", name="total_price", type="number", step="0.01", min="0"),
                LabelSelect(*[Option(status, value=status) for status in statuses], label="Booking Status", name="status"),
            ),
            Grid(
                LabelSelect(*[Option(pm, value=pm) for pm in payment_methods], label="Payment Method", name="payment_method"),
                LabelInput("Reference Number", name="reference_number", placeholder="Required for eCash"),
            ),
            DivCentered(Button("Submit Booking", cls=ButtonT.primary)),
        ),
        Div(id="form-status", cls="mt-4")  
    )


# ==============================
# 📌 Submit Booking (Converts `room_number` to `room_id` Before Storing)
# ==============================

async def submit_booking(req):
    """Handles booking form submission and inserts data into Supabase."""
    try:
        form_data = await req.form()

        room_number = form_data.get("room_number", "").strip()

        # Convert Room Number to Room ID
        room_response = supabase.table("rooms").select("id").eq("room_number", room_number).execute()
        if not room_response.data:
            return Alert(f"Validation Error: Room {room_number} not found.", cls=AlertT.warning)
        
        room_id = UUID(room_response.data[0]["id"])  

        # Extract other values safely
        booking = BookingModel(
            room_number=room_number,
            guest_name=form_data.get("guest_name", ""),
            guest_email=form_data.get("guest_email", ""),
            guest_phone=form_data.get("guest_phone", ""),
            check_in_date=date.fromisoformat(form_data.get("check_in_date", str(date.today()))),
            check_out_date=date.fromisoformat(form_data.get("check_out_date", str(date.today()))),
            number_of_guests=int(form_data.get("number_of_guests", 1)),  
            total_price=float(form_data.get("total_price", 0.0)),  
            status=form_data.get("status", "Pending"),
            payment_method=form_data.get("payment_method", "Cash"),
            reference_number=form_data.get("reference_number", None),
        )

        # Convert `date` fields to ISO format before inserting
        booking_data = booking.model_dump()
        booking_data["check_in_date"] = booking.check_in_date.isoformat()
        booking_data["check_out_date"] = booking.check_out_date.isoformat()
        booking_data["total_price"] = float(booking.total_price)  
        booking_data["room_id"] = str(room_id)  

        # ✅ Fix: Ensure NULL reference_number for Cash payments
        booking_data["reference_number"] = (
            None if booking.payment_method == "Cash" else booking.reference_number
        )

        response = supabase.table("bookings").insert(booking_data).execute()

        if response.data:
            return Div(  
                Alert("Booking successfully added!", cls=AlertT.success),
                Script("document.querySelector('form').reset();")  
            )
        else:
            return Alert("Failed to add booking. Please try again.", cls=AlertT.error)

    except ValueError as ve:
        return Alert(f"Validation Error: {ve}", cls=AlertT.warning)
    except Exception as e:
        return Alert(f"Error: {str(e)}", cls=AlertT.error)


# ==============================
# 📌 Run the FastHTML Server
# ==============================
