from fasthtml.common import *
from monsterui.all import *
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from uuid import UUID, uuid4

from db_connection import supabase as db

# ==============================
# 📌 Load Environment Variables
# ==============================


supabase = db

BUCKET_NAME = "room-images"
ROOM_TYPES = ["Standard", "Family", "Deluxe"]


class Room(BaseModel):
    room_number: str = Field(..., min_length=1, max_length=50)
    room_type: str = Field(...)
    description: str = Field(...)
    max_guests: int = Field(..., gt=0)
    status: str = Field(...)
    price_per_night: float = Field(..., gt=0)
    image_id: str | None = None  # Stores image path

def room_form():
    return Titled("Room Registration Form",
        Form(method="post", action="/submit_room", enctype="multipart/form-data", 
     hx_post="/submit_room", hx_target="#result-table", hx_swap="outerHTML")(
            Grid(
                LabelInput("Room Number", name="room_number"),
                LabelSelect(*[Option(rt, value=rt) for rt in ROOM_TYPES], label="Room Type", name="room_type")),
            LabelInput("Description", name="description"),
            Grid(
                LabelInput("Max Guests", name="max_guests", type="number"),
                LabelInput("Price per Night", name="price_per_night", type="number", step="0.01")),
            LabelSelect(*[Option(st, value=st) for st in ["Available", "Occupied", "Under Maintenance"]], label="Status", name="status"),
            Label("Upload Image"),
            Div(cls="flex items-center gap-2")(
                Upload(name="image", id="image-upload", accept=".png,.jpg,.jpeg,.heic", cls="hidden"),
                Button(UkIcon('upload'), type="button", cls=ButtonT.primary, onclick="document.getElementById('image-upload').click()")
            ),
            DivCentered(Button("Submit Form", type="submit", cls=ButtonT.primary))
        ),
        Div(id="result-table", cls="mt-6")
    )


async def submit_rooms(req):
    try:
        form_data = await req.form()
        form_data = dict(form_data)
        file = form_data.get("image")
        image_id = None

        if file and hasattr(file, "filename"):
            file_ext = file.filename.split(".")[-1]
            unique_filename = f"room_images/{uuid4()}.{file_ext}"
            file.file.seek(0)
            file_data = file.file.read()
            
            response = supabase.storage.from_(BUCKET_NAME).upload(unique_filename, file_data, file_options={"content-type": f"image/{file_ext}"})
            
            if hasattr(response, "error") and response.error:
                return P(f"Image Upload Error: {response.error.message}", cls=TextT.error)
            
            # ✅ Save only the filename (UUID + extension)
            image_id = unique_filename.split("/")[-1]

        form_data["image_id"] = image_id
        data = Room(**form_data)
        response = supabase.table("rooms").insert(data.dict(exclude_none=True)).execute()
        
        if hasattr(response, "error") and response.error:
            return P(f"Database Error: {response.error.message}", cls=TextT.error)

        return Div(
    Alert("Room successfully added!", cls=AlertT.success),room_table())
    except Exception as e:
        return P(f"Error: {str(e)}", cls=TextT.error)


def room_table():
    response = supabase.table("rooms").select("*").execute()
    rooms = response.data
    
    if not rooms:
        return Div(id="result-table", cls="mt-6", children=[P("No rooms registered yet.", cls=TextT.muted)])
    
    return Div(id="result-table", cls="mt-6", children=[
        Table(
            Tr(Th("Room Number"), Th("Room Type"), Th("Description"), Th("Max Guests"), Th("Status"), Th("Price per Night"), Th("Image")),
            *[Tr(*[
                Td(str(room[field])) for field in ["room_number", "room_type", "description", "max_guests", "status", "price_per_night"]
            ] + [
                Td(Img(src=supabase.storage.from_(BUCKET_NAME).get_public_url(f"room_images/{room['image_id']}")) 
                   if room["image_id"] else "No Image")
            ]) for room in rooms]
        )
    ])



