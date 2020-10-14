from app import db

class Traceback(db.Model):
    __tablename__ = 'traceback'

    id = db.Column(db.Integer, db.Sequence('trackeback_id_seq'), primary_key = True)
    date = db.Column(db.String)
    host = db.Column(db.String)
    app = db.Column(db.String)
    tb = db.Column(db.String)
    tp = db.Column(db.String)
    vl = db.Column(db.String)

    def __init__(self, date, host, app, tb, tp, vl):
        self.date = date
        self.host = host
        self.app = app
        self.tb = tb
        self.tp = tp
        self.vl = vl

    def __repr(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
                'id': self.id,
                'date': self.date,
                'host': self.host,
                'app': self.app,
                'tb': self.tb,
                'tp': self.tp,
                'vl': self.vl
            }