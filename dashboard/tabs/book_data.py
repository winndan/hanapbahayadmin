from fasthtml.common import *  # Import FastHTML components# Used to get unstyled components
from monsterui.all import *  # Import MonsterUI for styled components
from fasthtml.svg import *
from dashboard.table.bookings import booking_table
from dashboard.table.rooms import room_table


def BookData():
    return Div(
        booking_table(),
        cls="p-4 overflow-auto w-full"
    )

