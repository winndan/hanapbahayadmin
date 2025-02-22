from fasthtml.common import *
from monsterui.all import *
from dashboard.admin import admin_dash
from homepage.homepage import homepage


app, rt = fast_app(hdrs=Theme.slate.headers(daisy=True), live=True)


# Frontend

@rt("/")
async def get_homepage():
    return homepage()


@rt("/admin")
async def admin_page():
    return admin_dash()
 

if __name__ == "__main__":
    serve()
