from fasthtml.common import *
from monsterui.all import *
from dashboard.dashboard import admin_dash


app, rt = fast_app(hdrs=Theme.slate.headers(daisy=True), live=True)


# Frontend

@rt("/")
async def get_homepage():
    return P("Home testing")


@rt("/admin")
async def admin_page():
    return admin_dash()
 

if __name__ == "__main__":
    serve()
