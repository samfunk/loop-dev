import os
import operator
import re
import json
from flask import Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from collections import Counter


app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS') or 'config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from models import *


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/new_model", methods=['GET', 'POST'])
def new_model():
    return 'OK'

@app.route("/model/<model_id>/new_point", methods=['GET', 'POST'])
def new_point(model_id):
    return 'OK'

if __name__ == '__main__':
    app.run()
