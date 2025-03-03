from fasthtml.common import *
from fasthtml.components import Uk_input_tag
from fasthtml.svg import *
from monsterui.all import *

app, rt = fast_app(hdrs=Theme.blue.headers(),  favicon="/assets/favicon.ico")

# JavaScript function to toggle password visibility
toggle_password_script = """
document.addEventListener('DOMContentLoaded', function () {
    let toggleBtn = document.getElementById('toggle-password');
    let pwd = document.getElementById('password');

    if (toggleBtn) {
        toggleBtn.addEventListener('click', function () {
            if (pwd.type === 'password') {
                pwd.type = 'text';
            } else {
                pwd.type = 'password';
            }
        });
    }
});
"""

CreateAccount = Card(
    DividerSplit("Bukana Admin", text_cls=TextPresets.muted_sm),
    LabelInput('Email', id='email', placeholder='m@example.com'),
    Div(
        Input(id='password', placeholder='Password', type='password', cls='flex-1'),
        Button(UkIcon('eye'), id='toggle-password', cls='ml-2', type='button'),
        cls='flex items-center'
    ),
    header=Div(Img(src='/assets/logo.png', alt='Logo', cls='mx-auto w-32 h-32'), cls='flex justify-center'),
    footer=Button('Signin', type="submit", cls=(ButtonT.primary, 'w-full'), hx_post="/login", hx_target="#response")
)


@rt
def index():
    return Title("Bukana | Admin"), Favicon("/assets/favicon.ico", "/assets/favicon.ico"),Container(Div(CreateAccount, cls='space-y-4')), Script(toggle_password_script)

serve()
