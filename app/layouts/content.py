from dash import html, dcc
import dash_bootstrap_components as dbc
import datetime

from app.config.config import Config

config = Config()

base = datetime.datetime.today()

def generate_card_content(n):
    card_content = [
        dbc.CardBody(dcc.Graph(id="kpi%s"%n,style={"height":"110px"}), ),
    ]
    return card_content

from app.utils.load_info import load_info
_, devices = load_info()

devices_ordered = {device["name"]: device["tag"] for device in devices}
devices_ordered = dict(sorted(devices_ordered.items()))

layout = [   
            dcc.Interval(id="time_interval_content", interval=2*1000, n_intervals=1, disabled=True),
            dbc.Row([
                dbc.Col([
                    dbc.Card(generate_card_content(1),),
                ],
                className="pt-3", width=3, style={"min-width":"250px"}),
                dbc.Col([
                    dbc.Card(generate_card_content(2),),
                ],
                className="pt-3", width=3, style={"min-width":"250px"}),
                dbc.Col([
                    dbc.Card(generate_card_content(3),),
                ],
                className="pt-3", width=3, style={"min-width":"250px"}),
                dbc.Col([
                    dbc.Card(generate_card_content(4),),
                ],
                className="pt-3", width=3, style={"min-width":"250px"})
            ],),
            dbc.Row([
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                html.H5("Power measurements", className="card-title"),
                                dcc.Dropdown(
                                    id='elec_groups',
                                    options=[{'label':k, 'value': v} for k, v in devices_ordered.items()],
                                    value=[devices[0]['tag']],
                                    multi=True
                                ),
                                dcc.Dropdown(
                                    id='sensor_type',
                                    options=[{'label':sensor, 'value':i} for i, sensor in enumerate(["Apparent Power", "Active Power"])
                                    ],
                                    value=[1],
                                    multi=True
                                ), 
                                dcc.Graph(id="power_graph", style={"height": "55%"}, className="loading"),
                                dcc.Slider(
                                    id="day_slider",
                                    min=1,
                                    max=7,
                                    value=1,
                                    marks={
                                        1: {'label':"1 day"},
                                        3: {'label':"3 days"},
                                        5: {'label':"5 days"},
                                        7: {'label':"7 days"},
                                    }
                                )
                                ], style={"height": "100%", "overflow-y": "auto"}
                            ), style={"height": "45vh"}
                        )],
                        width=6, className="pt-3 pr-0"
                    ),
                    dbc.Col([
                            dbc.Card(
                                dbc.CardBody([
                                    html.H5("Energy proportion by process", className="card-title"),
                                    dcc.Graph(id="overall_process", style={"height": "80%"}, className="loading")
                                ], style={"height": "100%", "overflow-y": "auto"})
                            , style={"height": "45vh"})
                    ],
                        width=6, className="pt-3"
                    ),
                ], align="stretch"
            ),
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Select date and time range"),
                            html.Div(id="datetime_feedback"),
                            html.B(html.P("Start datetime", className="mb-2")),
                            html.Div(dcc.Input(
                                id="start_date",
                                type='text',
                                value=(datetime.date.today()-datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M"),
                            ), className="mb-4"),
                            html.B(html.P("End datetime", className="mb-2")),
                            html.Div(dcc.Input(
                                id="end_date",
                                type='text',
                                value=datetime.date.today().strftime("%Y-%m-%dT%H:%M"),
                            ), className="mb-4"),
                            html.B(html.P("{}Wh/€".format(config.DISPLAY_UNIT), className="mb-2")),
                            html.Div(dcc.Input(id="input1"), className="mb-5"),
                            html.Div(html.Button('Refresh', id='button', n_clicks=0))],
                        ),
                        style={"height": "100%"}),
                    width=4,  style={"height":"100%"}, className="pt-3"),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("{}Wh consumption for all measurements".format(config.DISPLAY_UNIT), className="card-title"),                        
                            dcc.Graph(id="comparison_plot", style={"height": "40vh"}, className="loading"),
                        ], style={"height": "100%","overflow-y": "auto"}
                        ), 
                    style={"height": "100%"}),
                    width=8,  style={"height":"100%"}, className="pt-3"
                ),
            ], align="stretch"
            ),
            dbc.Row(
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Factory energy flow", className="card-title"),
                            dcc.Graph(id="sankey_diagram", style={"height": "680px"}, className="loading")
                        ], style={"height": "100%"})
                    , style={"height": "100%"}
                    )], className="pt-3",
            ))
        ]