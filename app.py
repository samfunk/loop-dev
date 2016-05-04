import os
import operator
import re
import json
import uuid

from flask import Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.uuid import FlaskUUID
from collections import Counter

from lib.utils import make_grid

from models import *


app = Flask(__name__)
FlaskUUID(app)
app.config.from_object(os.getenv('APP_SETTINGS') or 'config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/new_model", methods=['POST'])
def new_model():
    data = request.get_json() or {}
    if not data:
        return jsonify(exception="Invalid data POSTed to /exists")

    new_model_id = uuid.uuid4()
    grid = make_grid(data, new_model_id)
    return jsonify(id=new_model_id)


@app.route("/report_metric/<uuid:model_id>")
def report_metric():
    return "OK"


@app.route("/new_iteration/<uuid:model_id>", methods=['POST'])
def new_point(model_id):
    return 'OK'

if __name__ == '__main__':
    app.run()
