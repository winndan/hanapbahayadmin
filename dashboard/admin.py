from fasthtml.common import *  # Import FastHTML components
import fasthtml.common as fh  # Used to get unstyled components
from monsterui.all import *  # Import MonsterUI for styled components
from fasthtml.svg import *

def InfoCard(title, value, change):
    return Card(H3(value), P(change, cls=TextPresets.muted_sm), header=H4(title))

info_card_data = [
    ("Total Revenue", "$45,231.89", "+20.1% from last month"),
    ("Subscriptions", "+2,350", "+180.1% from last month"),
    ("Sales", "+12,234", "+19% from last month"),
    ("Active Now", "+573", "+201 since last hour")
]

top_info_row = Grid(*[InfoCard(*row) for row in info_card_data])

def AvatarItem(name, email, amount):
    return DivFullySpaced(
        DivLAligned(
            DiceBearAvatar(name, 9, 9),
            Div(Strong(name, cls=TextT.sm), Address(A(email, href=f'mailto:{email}')))
        ),
        fh.Data(amount, cls="ml-auto font-medium", value=amount[2:])
    )

recent_sales = Card(
    Div(cls="space-y-8")(
        *[AvatarItem(n, e, d) for (n, e, d) in (
            ("Olivia Martin", "olivia.martin@email.com", "+$1,999.00"),
            ("Jackson Lee", "jackson.lee@email.com", "+$39.00"),
            ("Isabella Nguyen", "isabella.nguyen@email.com", "+$299.00"),
            ("William Kim", "will@email.com", "+$99.00"),
            ("Sofia Davis", "sofia.davis@email.com", "+$39.00")
        )]
    ),
    header=Div(H3("Recent Sales"), Subtitle("You made 265 sales this month.")),
    cls='col-span-3'
)

def OverviewTab():
    return Div(
        H2("Dashboard Overview"),
        top_info_row,
        recent_sales
    )


    
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
            Li(A("Analytics", href="#", hx_get="/tabs/analytics", hx_target="#tab-content")),
            Li(A("Reports", href="#", hx_get="/tabs/reports", hx_target="#tab-content")),
            Li(A("Notifications", href="#", hx_get="/tabs/notifications", hx_target="#tab-content")),
            alt=True
        ),
        Div(OverviewTab(), id="tab-content"),  # Default content
        cls=('space-y-4', ContainerT.xl)
    )
