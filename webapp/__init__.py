import os
from webapp.constants import types
from webapp.json_handler_helper import load_json, get_json_path, get_keys_by_suffix, \
    find_all_fields_by_suffix, get_not_date_reflect_fields

from flask import Flask, abort, json, current_app as app, jsonify, request

from flask_basicauth import BasicAuth
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['BASIC_AUTH_USERNAME'] = 'kris'
app.config['BASIC_AUTH_PASSWORD'] = 'secret_key'
basic_auth = BasicAuth(app)

CORS(app, expose_headers='Authorization')

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per minute"]
)

file_path = get_json_path(app.static_folder, 'dashboard.json')
dashboard_data = load_json(file_path)

get_not_date_reflect_fields(dashboard_data)


@app.route('/get-dashboard', methods=['POST'])
@basic_auth.required
def get_dashboard():
    type = request.json['type']
    return jsonify(find_all_fields_by_suffix(dashboard_data, types[type], type))
