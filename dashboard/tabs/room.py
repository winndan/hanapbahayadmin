from fasthtml.common import *  # Import FastHTML components# Used to get unstyled components
from monsterui.all import *  # Import MonsterUI for styled components
from fasthtml.svg import *
from dashboard.forms.rooms import room_form


def RoomTab():
    return room_form()
