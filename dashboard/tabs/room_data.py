from fasthtml.common import *  # Import FastHTML components# Used to get unstyled components
from monsterui.all import *  # Import MonsterUI for styled components
from fasthtml.svg import *
from dashboard.table.bookings import booking_table
from dashboard.table.rooms import room_table


def RoomData():
    return Div(
        room_table(),
        cls="p-4 overflow-auto w-full"
    )

