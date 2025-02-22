from fasthtml.common import *
from monsterui.all import *

def homepage():
    return Html(
        Head(
            Meta(charset='UTF-8'),
            Meta(http_equiv='X-UA-Compatible', content='IE=edge'),
            Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
            Link(href='https://cdn.jsdelivr.net/npm/remixicon@3.2.0/fonts/remixicon.css', rel='stylesheet'),
            Title('Bukana | Booking'),
            Script(src="https://unpkg.com/htmx.org@2.0.4")
        ),
        Body( 
            Nav(P("test")
                
            )
        ),
        lang='en',
        hx_boost="true" 
    )
