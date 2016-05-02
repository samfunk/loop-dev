import os
import requests
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


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    return 'hello'

if __name__ == '__main__':
    app.run()
