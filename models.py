import pandas as pd

from app import db
from sqlalchemy.dialects.postgresql import JSONB


class ModelGrid(db.Model):
    __tablename__ = 'model_grids'

    id = db.Column(db.String(), primary_key=True)
    grid = db.Column(JSONB)
    chooser = db.Column(db.String())
    minimize = db.Column(db.Boolean)

    def __init__(self, id, grid, chooser, minimize=False):
        self.id = id
        self.grid = grid
        self.minimize = minimize
        self.chooser = chooser

    def get_grid(self):
        return pd.read_json(self.grid)

    def __repr__(self):
        return '<model_grid {} of cardinality {}>'.format(self.id, pd.read_json(self.grid).shape)
