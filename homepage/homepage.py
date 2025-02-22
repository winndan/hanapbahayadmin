from fasthtml.common import *
from monsterui.all import *

def homepage():
    return Html(
        Head(
            Meta(charset='UTF-8'),
            Meta(http_equiv='X-UA-Compatible', content='IE=edge'),
            Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
            Link(href='https://cdn.jsdelivr.net/npm/remixicon@3.2.0/fonts/remixicon.css', rel='stylesheet'),
            Link(rel='stylesheet', href='styles/styles.css'),
            Title('Bukana | Booking'),
            Script(src="https://unpkg.com/htmx.org@2.0.4")
        ),
        Body( 
            Nav(
                Div(
                    'Bukana',
                    Span('.'),
                    cls='nav__logo'
                ),
                Ul(
                    Li(A('Home', href='#'), cls='link'),
                    Li(A('Rooms', href='#'), cls='link'),
                    Li(A('How to use', href='#'), cls='link'),
                    Li(A('Reviews', href='#'), cls='link'),
                    cls='nav__links'
                ),
                Button(
                "Sign Up",
                cls='btn',
                onclick="window.location.href='/signup';"  # ✅ Full page reload
            )

            ),
            Header(
                Div(
                    Div(
                        Img(src='assets/header--1.jpg', alt='header'),
                        Img(src='assets/header--2.jpg', alt='header'),
                        cls='header__image'
                    ),
                    Div(
                        Div(
                            P('Your Perfect Room Awaits – Book It in a Snap ✨', cls='sub__header'),
                            H1('Rooms That Feel Like Home'),
                            P('From Cozy Nooks to Luxurious Suites, Find the Ideal Room for Every Stay – Because Where You Rest Matters.', cls='section__subtitle'),
                            Div(
                                Button('Login', cls='btn',
                                       onclick="window.location.href='/signin';"),
                                Div(
                                    Div(
                                        Img(src='assets/story.jpg', alt='story'),
                                        Span(I(cls='ri-play-fill')),
                                        cls='video__image'
                                    ),
                                    Span('Watch our story'),
                                    cls='story'
                                ),
                                cls='action__btns'
                            )
                        ),
                        cls='header__content'
                    ),
                    cls='section__container header__container'
                )
            ),
            Section(
                Div(
                    Div(
                        H2('Endless Room Options', cls='section__title'),
                        P('Whether you need a budget-friendly single or a lavish suite, we’ve got rooms for every taste and budget.', cls='section__subtitle')
                    ),
                    Div(
                        Span(I(cls='ri-arrow-left-s-line')),
                        Span(I(cls='ri-arrow-right-s-line')),
                        cls='destination__nav'
                    ),
                    cls='section__header'
                ),
                Div(
                    *[
                        Div(
                            Img(src=f'assets/room{i}.jpg', alt='destination'),
                            Div(
                                P(name, cls='destination__title'),
                                P(location, cls='destination__subtitle'),
                                cls='destination__details'
                            ),
                            cls='destination__card'
                        ) for i, (name, location) in enumerate([
                            ('Banff', 'Canada'),
                            ('Machu Picchu', 'Peru'),
                            ('Lauterbrunnen', 'Switzerland'),
                            ('Zhangjiajie', 'China')
                        ], start=1)
                    ],
                    cls='destination__grid'
                ),
                cls='section__container destination__container'
            ),
            Section(
                Div(
                    H2('Subscribe to get special prizes', cls='section__title'),
                    P('Sign up to receive exclusive travel deals and updates.', cls='section__subtitle'),
                    Form(
                        Input(type='email', placeholder='Your email here'),
                        Button('Send', type='submit', cls='btn'),
                        cls='subscribe__form'
                    ),
                    cls='section__container subscribe__container'
                ),
                cls='subscribe'
            ),
            Footer(
                Div(
                    Div(
                        H3('Bukana', Span('.')),
                        P('Your gateway to the best travel experiences worldwide.'),
                        cls='footer__col'
                    ),
                    Div(
                        H4('Support'),
                        P('FAQs'),
                        P('Terms & Conditions'),
                        P('Privacy Policy'),
                        P('Contact Us'),
                        cls='footer__col'
                    ),
                    Div(
                        H4('Address'),
                        P(Span('Address:'), '280 Wilson Street, Cima, California, USA'),
                        P(Span('Email:'), 'info@bukana.com'),
                        P(Span('Phone:'), '+1 9876543210'),
                        cls='footer__col'
                    ),
                    cls='section__container footer__container'
                ),
                Div('Copyright © 2025 Bukana. All rights reserved.', cls='footer__bar'),
                cls='footer'
            )
        ),
        lang='en',
        hx_boost="true" 
    )
