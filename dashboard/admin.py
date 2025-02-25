from fasthtml.common import *  # Import FastHTML components
import fasthtml.common as fh  # Used to get unstyled components
from monsterui.all import *  # Import MonsterUI for styled components
from fasthtml.svg import *
from dashboard.tabs.overview import OverviewTab

    
def NavSpacedLi(t,s): return NavCloseLi(A(DivFullySpaced(P(t),P(s,cls=TextPresets.muted_sm))))
avatar_dropdown = Div(
      DiceBearAvatar('Alicia Koch',8,8),
      DropDownNavContainer(
          NavHeaderLi('sveltecult',NavSubtitle("leader@sveltecult.com")),
          ))


top_nav = NavBar(
     *map(lambda text: Button(
    text, 
    cls=ButtonT.ghost, 
    hx_get="/profile" if text == "Profile" else None,  # Load Profile Page with HTMX
    hx_post="/logout" if text == "Logout" else None,  # Logout with HTMX
    hx_target="body" if text == "Logout" else None  # Apply HTMX response to the body (optional)
), ["Profile", "Logout"]),
    brand=DivLAligned(avatar_dropdown))



def admin_dash():
    return Title("Dashboard Example"), Container(
        top_nav,
        TabContainer(
            Li(A("Overview", href="#", hx_get="/tabs/overview", hx_target="#tab-content", cls='uk-active')),
            Li(A("Booking", href="#", hx_get="/tabs/book", hx_target="#tab-content")),
            Li(A("Room", href="#", hx_get="/tabs/room", hx_target="#tab-content")),
            Li(A("Payment", href="#", hx_get="/tabs/payment", hx_target="#tab-content")),
            alt=True
        ),
        Div(OverviewTab(), id="tab-content"),  # Default content
        cls=('space-y-4', ContainerT.xl)
    )
