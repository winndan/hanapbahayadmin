from fasthtml.common import *  
from monsterui.all import *  
from fasthtml.svg import *
from dashboard.tabs.overview import OverviewTab
from dashboard.tabs.book import BookTab
from dashboard.tabs.room import RoomTab
from dashboard.tabs.book_data import BookData
from dashboard.tabs.room_data import RoomData


# ✅ Custom Spaced List Item
def NavSpacedLi(t, s): 
    return NavCloseLi(A(DivFullySpaced(P(t), P(s, cls=TextPresets.muted_sm))))

# ✅ Avatar Dropdown
avatar_dropdown = Div(
    DiceBearAvatar('Alicia Koch', 8, 8),
    DropDownNavContainer(
        NavHeaderLi('Admin Account'),
    )
)

# ✅ Navbar with "Profile" and "Logout"
top_nav = NavBar(
    *map(lambda text: Button(
        text, 
        cls=ButtonT.ghost, 
        hx_post="/logout" if text == "Logout" else None,  
        hx_target="body" if text == "Logout" else None  
    ), ["Logout"]),
    brand=DivLAligned(avatar_dropdown)
)

# ✅ Function to Load Tab Content
def load_tab_content(tab):
    tabs = {
        "overview": OverviewTab,
        "add-book": BookTab,
        "add-room": RoomTab,
        "book-data": BookData,
        "room-data": RoomData
    }
    return tabs.get(tab, lambda: H1("Tab Not Found"))()  

# ✅ Admin Dashboard with Navbar & Dynamic Tabs
def admin_dash(active_tab="overview"):  
    return Div(
        top_nav,  # ✅ Include Navbar
        Container(
            TabContainer(
                Li(A("Overview",  
                      href="#", hx_get=f"/admin?tab=overview", hx_target="#admin-content", hx_push_url="true",
                      cls=f"px-4 py-2 {'uk-active bg-slate-500 text-white' if active_tab == 'overview' else 'hover:bg-gray-200'}")),
                Li(A("Book",  
                      href="#", hx_get=f"/admin?tab=add-book", hx_target="#admin-content", hx_push_url="true",
                      cls=f"px-4 py-2 {'uk-active bg-slate-500 text-white' if active_tab == 'add-book' else 'hover:bg-gray-200'}")),
                Li(A("Room",  
                      href="#", hx_get=f"/admin?tab=add-room", hx_target="#admin-content", hx_push_url="true",
                      cls=f"px-4 py-2 {'uk-active bg-slate-500 text-white' if active_tab == 'add-room' else 'hover:bg-gray-200'}")),
                Li(A("Book Data",  
                      href="#", hx_get=f"/admin?tab=book-data", hx_target="#admin-content", hx_push_url="true",
                      cls=f"px-4 py-2 {'uk-active bg-slate-500 text-white' if active_tab == 'book-data' else 'hover:bg-gray-200'}")),
                Li(A("Room Data",  
                      href="#", hx_get=f"/admin?tab=room-data", hx_target="#admin-content", hx_push_url="true",
                      cls=f"px-4 py-2 {'uk-active bg-slate-500 text-white' if active_tab == 'room-data' else 'hover:bg-gray-200'}")),
                alt=True
            ),
            Div(load_tab_content(active_tab), id="tab-content"),  
            cls=('space-y-4', ContainerT.xl)
        ), id="admin-content"
    )
