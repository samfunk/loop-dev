from app import db
from sqlalchemy.dialects.postgresql import JSONB


class ModelGrid(db.Model):
    __tablename__ = 'model_grids'

    id   = db.Column(db.String(), primary_key=True)
    grid = db.Column(JSONB)

    def __init__(self, id, grid):
        self.id = id
        self.grid = grid

    def __repr__(self):
        return '<id {}>'.format(self.id)
