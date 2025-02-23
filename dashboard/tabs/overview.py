from fasthtml.common import *
import fasthtml.common as fh
from monsterui.all import *
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
