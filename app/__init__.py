import dash
import dash_bootstrap_components as dbc
from flask import Flask

from .layouts.index import layout_index

from .callbacks.callbacks import init_callbacks

server = Flask(__name__)

app = dash.Dash(__name__, 
                meta_tags=[{"name": "viewport", "content": "width=device-width"}], 
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                assets_folder="assets/",
                suppress_callback_exceptions=True,
                title="Energy Management Dashboard",
                update_title=None,
                server=server)

app.layout = layout_index

init_callbacks(app)
    
if __name__ == '__main__':
    app.run_server()