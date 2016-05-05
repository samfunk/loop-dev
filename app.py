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
        chooser = data.get("chooser") or DEFAULT_CHOOSER
        if chooser not in list(LIST_OF_CHOOSERS.keys()):
            error_string = """The chooser <{}> that you've supplied is not yet implemented.
                You can find the list of available choosers by querying /choosers endpoint."""
            return jsonify(exception=error_string.format(chooser))
        db.session.add(ModelGrid(new_model_id, grid.to_json(), chooser, minimize))
        db.session.commit()
    except:
        raise TypeError("Unable to add item to database.")
    return jsonify(id=new_model_id, grid_size=grid.shape, chooser=chooser, minimize=minimize)


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
    except:
        raise TypeError("Unable to find a model with uuid {} in the database.".format(id))
    return jsonify(status="ok")


@app.route("/choosers", methods=['GET', 'POST'])
def choosers():
    return jsonify(choosers=list(LIST_OF_CHOOSERS.keys()))


@app.route("/new_iteration/<uuid:id>", methods=['GET', 'POST'])
def new_point(id):
    try:
        modelgrid = db.session.query(ModelGrid).filter_by(id=str(id)).first()
        candidates = modelgrid.get_grid()
    except:
        return jsonify(exception="Unable to find a model with uuid {} in the database.".format(id))

    acquisition_function = LIST_OF_CHOOSERS[modelgrid.chooser]
    selected_row = acquisition_function(candidates)
    if selected_row is None:
        error_string = "There are no more candidates left in the grid. Maybe start a new search?"
        return jsonify(exception=error_string)
    candidates.loc[candidates._loop_id == selected_row, "_loop_status"] = "pending"
    params = candidates.loc[candidates._loop_id == selected_row, :].to_dict(orient='records')[0]
    params = {k: v for k, v in params.items() if not k.startswith('_loop')}
    try:
        modelgrid.grid = candidates.to_json()
        db.session.commit()
    except:
        error_string = "Unable to update the model grid in the database for an unknown reason."
        return jsonify(exception=error_string)
    return jsonify(params=params)

if __name__ == '__main__':
    app.run()
