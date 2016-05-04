import os
import operator
import math
import re
import json
import uuid

from flask import Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.uuid import FlaskUUID
from collections import Counter

from lib.make_grid import make_grid
from lib.choosers import *


app = Flask(__name__)
FlaskUUID(app)
app.config.from_object(os.getenv('APP_SETTINGS') or 'config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from models import *


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/new_model", methods=['POST'])
def new_model():
    data = request.get_json() or {}
    if not data:
        return jsonify(exception="Invalid data POSTed to /new_model")
    try:
        grid = make_grid(data)
        new_model_id = uuid.uuid4()
        minimize = data.get("minimize") or False
        db.session.add(ModelGrid(new_model_id, grid.to_json(), minimize))
        db.session.commit()
    except:
        raise TypeError("Unable to add item to database.")
    return jsonify(id=new_model_id, grid_size=grid.shape, minimize=minimize)


@app.route("/report_metric/<uuid:id>", methods=['POST'])
def report_metric(id):
    data = request.get_json() or {}
    if not data:
        return jsonify(exception="Invalid data POSTed to /report_metric")
    if not data.get("value"):
        return jsonify(exception="Must supply a <value> to /report_metric route")
    if not data.get("loop_id"):
        return jsonify(exception="Must supply a <loop_id> to /report_metric route")
    try:
        modelgrid = db.session.query(ModelGrid).filter_by(id=str(id)).first()
        candidates = modelgrid.get_grid()

        if not candidates.loc[candidates._loop_id == data.get('loop_id'), :].shape[0]:
            error_string = "No set of parameters corresponding to your id of {} found."
            return jsonify(exception=error_string.format(data.get('loop_id')))
        if not math.isnan(candidates.loc[candidates._loop_id == data.get('loop_id'), "_loop_value"]):
            error_string = "There is already a score of {} associated with this set of parameters"
            score = candidates.loc[candidates._loop_id == data.get('loop_id'), "_loop_value"]
            return jsonify(exception=error_string.format(round(float(score), 2)))

        candidates.loc[candidates._loop_id == data.get('loop_id'), "_loop_value"] = data.get("value")
        candidates.loc[candidates._loop_id == data.get('loop_id'), "_loop_status"] = "complete"
        if data.get("duration"):
            candidates.loc[candidates._loop_id == data.get('loop_id'),
                           "_loop_duration"] = data.get("duration")

        modelgrid.grid = candidates.to_json()
        db.session.commit()
        print(candidates)
    except:
        raise TypeError("Unable to find a model with uuid {} in the database.".format(id))
    return jsonify(status="ok")


@app.route("/new_iteration/<uuid:model_id>", methods=['POST'])
def new_point(model_id):
    return 'OK'

if __name__ == '__main__':
    app.run()
