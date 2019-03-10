from app import db

class User(db.model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	#i is short for interval
	#defaults need to be changed
	snap_i = db.Column(db.Integer, default=0)
	fertilizing_i = db.Column(db.Integer, default=0)
	humidity_temp_i = db.Column(db.Integer, default=0)

	water_treshold = db.Column(db.Integer, default=0)
	water_amount = db.Column(db.Integer, default=0)
	fertilize_amount = db.Column(db.Integer, default=0)
	#pics = db.relationship('Pics', backref='user', lazy='dynamic')


class Pics(db.Model):
	id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(64), index=True, unique=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class Water(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	amount_watered = db.Column(db.Integer)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Fertilize(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	amount_fertilized = db.Column(db.Integer)
	timestamp = db.Column(db.Integer, default=datetime.utcnow)

class Humidity_temp(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	humidity = db.Column(db.Integer)
	temp = db.Column(db.Integer)
	timestamp = db.Column(db.Integer, default=datetime.utcnow)
		