import pandas as pd
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app import db


class ModelGrid(db.Model):
    __tablename__ = 'model_grids'

    id = db.Column(db.String(), primary_key=True, index=True)
    grid = db.Column(JSONB)
    name = db.Column(db.String())
    chooser = db.Column(db.String())
    minimize = db.Column(db.Boolean)
    submissions = relationship("Submission", backref="model_grids")

    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    def __init__(self, id, grid, chooser, name=None, minimize=False):
        self.id = id
        self.name = name
        self.grid = grid
        self.minimize = minimize
        self.chooser = chooser

    def get_grid(self):
        return pd.read_json(self.grid)

    def best_value(self):
        values = [x.value for x in self.submissions]
        which = min if self.minimize else max
        try:
            best = which(values)
        except:
            best = None
        return best

    def __repr__(self):
        return '<model_grid {} of cardinality {}>'.format(self.id, pd.read_json(self.grid).shape)


class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_id = db.Column(db.String(), ForeignKey('model_grids.id'), index=True)
    loop_id = db.Column(db.Integer())
    value = db.Column(db.Float())

    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, model_id, loop_id, value):
        self.loop_id = loop_id
        self.model_id = model_id
        self.value = value

    def __repr__(self):
        return '<Submission id: <{}> for model grid {} of value {} for row {}>'.format(self.id,
                                                                                       self.model_id,
                                                                                       self.value,
                                                                                       self.loop_id)
