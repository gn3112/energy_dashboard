from dash import html, dcc
import dash_bootstrap_components as dbc
import datetime

base = datetime.datetime.today()

navbar = dbc.Navbar(
    [
        dbc.NavbarBrand(
            dbc.Row(
                [
                    dbc.Col(html.Img(src="/assets/favicon.ico", height="120%", className="mr-4"), width=2),
                    dbc.Col(html.Span("Energy management dashboard", className="mr-4"), width=10)
                ]
            )
        ),
        html.Span(id="live_time", className="navbar-text")
    ]
)

layout_index = html.Div(
    [   dcc.Location(id="url", refresh=True),
        dcc.Interval(id="time_interval", interval=1*1000, n_intervals=0, disabled=True),
        html.Div([
            navbar,
            dbc.Container(id="page-content", fluid=True)
        ],
        ),
    ],
    id="main_container"
)