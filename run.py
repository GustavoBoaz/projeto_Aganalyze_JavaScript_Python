import os, dash
from analyze import create_app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = create_app()
app =  dash.Dash(__name__, server=server, url_base_pathname='/dashboard/', external_stylesheets=external_stylesheets)

from analyze.routes import *
from analyze.dashboard import *

if __name__ == '__main__':
    if os.environ.get('VCAP_SERVICES') is None: # running locally
        #PORT = 8080
        DEBUG = True
        app.run_server(debug=DEBUG)
    else:                                       # running on CF
        PORT = int(os.getenv("PORT"))
        DEBUG = False
        app.run_server(host='0.0.0.0', port=PORT, debug=DEBUG)