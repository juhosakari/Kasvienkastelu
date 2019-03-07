from app import db

class Pics(db.Model):
	id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(64), index=True, unique=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)