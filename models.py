from app import db
from sqlalchemy.dialects.postgresql import JSONB


class ModelGrid(db.Model):
    __tablename__ = 'model_grids'

    id   = db.Column(db.String(), primary_key=True)
    grid = db.Column(JSONB)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)
