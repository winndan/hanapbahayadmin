from fasthtml.common import *
from monsterui.all import *
from dashboard.admin import admin_dash
from homepage.homepage import homepage
from dashboard.tabs.overview import OverviewTab
from dashboard.tabs.analytics import AnalyticsTab
from dashboard.tabs.reports import ReportsTab
from dashboard.tabs.notifications import NotificationsTab



app, rt = fast_app(hdrs=Theme.slate.headers(daisy=True), live=True)


# Frontend

@rt("/")
async def get_homepage():
    return homepage()


@rt("/admin")
async def admin_page():
    return admin_dash()
 
@rt("/tabs/overview")
async def overview():
    return OverviewTab()

@rt("/tabs/analytics")
async def analytics():
    return AnalyticsTab()

@rt("/tabs/reports")
async def reports():
    return ReportsTab()

@rt("/tabs/notifications")
async def notifications():
    return NotificationsTab()

if __name__ == "__main__":
    serve()
