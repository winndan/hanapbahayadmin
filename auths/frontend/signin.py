from fasthtml.common import *
from monsterui.all import *

def admin_login_page():
    return Titled("Admin Login",
        DivCentered(
            Container(
                H3("Admin Login"),
                Form(
                    Input(name="email", placeholder="Enter your email", type="email", required=True, autocomplete="username"),
                    Input(name="password", placeholder="Enter your password", type="password", required=True, autocomplete="current-password"),
                    Button("Login", cls=ButtonT.primary, type="submit"),
                    hx_post="/admin-login",
                    hx_target="#login-error",
                    hx_swap="innerHTML",
                    cls="space-y-4"
                ),
                Div(id="login-error", cls="text-red-500"),
                cls="max-w-md mx-auto space-y-6"
            )
        )
    )
