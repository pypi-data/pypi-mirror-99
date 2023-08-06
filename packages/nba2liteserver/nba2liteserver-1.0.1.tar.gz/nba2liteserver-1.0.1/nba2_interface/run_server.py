from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from nba2_interface.route import app as route_mold
app.register_blueprint(route_mold, url_prefix="/")

SERVER_PORT = 3020

def run_server():
    app.run(host='0.0.0.0', port=SERVER_PORT, use_debugger=False, ssl_context='adhoc',
            use_reloader=False, passthrough_errors=True)

