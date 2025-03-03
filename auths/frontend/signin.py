from fasthtml.common import *
from fasthtml.components import Uk_input_tag
from fasthtml.svg import *
from monsterui.all import *

app, rt = fast_app(hdrs=Theme.blue.headers(), favicon="/assets/favicon.ico")

# 🔹 JavaScript function to toggle password visibility
toggle_password_script = """
document.addEventListener('DOMContentLoaded', function () {
    let toggleBtn = document.getElementById('toggle-password');
    let pwd = document.getElementById('password');

    if (toggleBtn) {
        toggleBtn.addEventListener('click', function () {
            pwd.type = (pwd.type === 'password') ? 'text' : 'password';
        });
    }
});
"""

# 🔹 Login Form Component
CreateAccount = Card(
    DividerSplit("Bukana Admin", text_cls=TextPresets.muted_sm),
    Form(  # ✅ Ensures HTMX sends form data
        LabelInput('Email', id='email', name="email", placeholder='m@example.com'),
        Div(
            Input(id='password', name="password", placeholder='Password', type='password', cls='flex-1'),
            Button(UkIcon('eye'), id='toggle-password', cls='ml-2', type='button'),
            cls='flex items-center'
        ),
        Button('Signin', type="submit", cls=(ButtonT.primary, 'w-full'), hx_post="/login", hx_target="#response"),
        Div(id="response", cls="text-red-500"),  # ✅ Displays error messages
        cls="space-y-4"
    ),
    header=Div(Img(src='/assets/logo-bg.png', alt='Logo', cls='mx-auto w-32 h-32'), cls='flex justify-center')
)

# 🔹 Login Page Function
def login_page():
    return Title("Bukana | Admin"), Favicon("/assets/favicon.ico","/assets/favicon.ico"), Container(Div(CreateAccount)), Script(toggle_password_script)
