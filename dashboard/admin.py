from fasthtml.common import *  # Import FastHTML components
import fasthtml.common as fh  # Used to get unstyled components
from monsterui.all import *  # Import MonsterUI for styled components
from fasthtml.svg import *
import pandas as pd

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

hotkeys = [('Profile', '⇧⌘P'), ('Billing', '⌘B'), ('Settings', '⌘S'), ('New Team', ''), ('Logout', '')]

def NavSpacedLi(t, s):
    return NavCloseLi(A(DivFullySpaced(P(t), P(s, cls=TextPresets.muted_sm))))

avatar_dropdown = Div(
    DiceBearAvatar('Alicia Koch', 8, 8),
    DropDownNavContainer(
        NavHeaderLi('sveltecult', NavSubtitle("leader@sveltecult.com")),
        *[NavSpacedLi(*hk) for hk in hotkeys],
    )
)

top_nav = NavBar(brand=DivLAligned(avatar_dropdown))

def admin_dash():
    return Title("Dashboard Example"), Container(
        top_nav,
        H2('Dashboard'),
        TabContainer(
            Li(A("Overview"), cls='uk-active'),
            *map(lambda x: Li(A(x)), ["Analytics", "Reports", "Notifications"]),
            alt=True
        ),
        top_info_row,
        Grid(
            recent_sales,  # Removed Plotly chart
            gap=4, cols_xl=7, cols_lg=7, cols_md=1, cols_sm=1, cols_xs=1
        ),
        cls=('space-y-4', ContainerT.xl)
    )
