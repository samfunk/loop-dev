import pandas as pd
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSONB

from app import db


class ModelGrid(db.Model):
    __tablename__ = 'model_grids'

    id = db.Column(db.String(), primary_key=True)
    grid = db.Column(JSONB)
    name = db.Column(db.String())
    chooser = db.Column(db.String())
    minimize = db.Column(db.Boolean)

    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, id, grid, chooser, name=None, minimize=False):
        self.id = id
        self.name = name if name else id
        self.grid = grid
        self.minimize = minimize
        self.chooser = chooser

    def get_grid(self):
        return pd.read_json(self.grid)

    def __repr__(self):
        return '<model_grid {} of cardinality {}>'.format(self.id, pd.read_json(self.grid).shape)
