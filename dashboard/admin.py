from fasthtml.common import *  
from monsterui.all import *  
from fasthtml.svg import *
from dashboard.tabs.overview import OverviewTab
from dashboard.tabs.book import BookTab
from dashboard.tabs.room import RoomTab
from dashboard.tabs.payment import PaymentTab

# ✅ Custom Spaced List Item
def NavSpacedLi(t, s): 
    return NavCloseLi(A(DivFullySpaced(P(t), P(s, cls=TextPresets.muted_sm))))

# ✅ Avatar Dropdown
avatar_dropdown = Div(
    DiceBearAvatar('Alicia Koch', 8, 8),
    DropDownNavContainer(
        NavHeaderLi('sveltecult', NavSubtitle("leader@sveltecult.com")),
    )
)

# ✅ Navbar with "Profile" and "Logout"
top_nav = NavBar(
    *map(lambda text: Button(
        text, 
        cls=ButtonT.ghost, 
        hx_get="/profile" if text == "Profile" else None,  
        hx_post="/logout" if text == "Logout" else None,  
        hx_target="body" if text == "Logout" else None  
    ), ["Profile", "Logout"]),
    brand=DivLAligned(avatar_dropdown)
)

# ✅ Function to Load Tab Content
def load_tab_content(tab):
    tabs = {
        "overview": OverviewTab,
        "book": BookTab,
        "room": RoomTab,
        "payment": PaymentTab
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
                      cls=f"px-4 py-2 {'uk-active bg-blue-500 text-white' if active_tab == 'overview' else 'hover:bg-gray-200'}")),
                Li(A("Booking",  
                      href="#", hx_get=f"/admin?tab=book", hx_target="#admin-content", hx_push_url="true",
                      cls=f"px-4 py-2 {'uk-active bg-blue-500 text-white' if active_tab == 'book' else 'hover:bg-gray-200'}")),
                Li(A("Room",  
                      href="#", hx_get=f"/admin?tab=room", hx_target="#admin-content", hx_push_url="true",
                      cls=f"px-4 py-2 {'uk-active bg-blue-500 text-white' if active_tab == 'room' else 'hover:bg-gray-200'}")),
                Li(A("Payment",  
                      href="#", hx_get=f"/admin?tab=payment", hx_target="#admin-content", hx_push_url="true",
                      cls=f"px-4 py-2 {'uk-active bg-blue-500 text-white' if active_tab == 'payment' else 'hover:bg-gray-200'}")),
                alt=True
            ),
            Div(load_tab_content(active_tab), id="tab-content"),  
            cls=('space-y-4', ContainerT.xl)
        ), id="admin-content"
    )
