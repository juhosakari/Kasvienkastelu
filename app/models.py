from app import db, login
from datetime import datetime
from flask_login import UserMixin

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	#i is short for interval
	#defaults need to be changed
	snap_i = db.Column(db.Integer, default=0)
	humidity_temp_i = db.Column(db.Integer, default=0)

	water_amount = db.Column(db.Integer, default=0)

	autowater = db.Column(db.Boolean, default=False)
	fertilized = db.Column(db.Boolean, default=False)

	water = db.relationship('Water', backref='user', lazy='dynamic')
	humidity_temp = db.relationship('Humidity_temp', backref='user', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.name)

class Pics(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String(64), index=True, unique=True)
	date = db.Column(db.Integer, index=True ,default=datetime.utcnow().timestamp())

class Water(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	amount_watered = db.Column(db.Integer)
	timestamp = db.Column(db.Integer,index=True , default=datetime.utcnow().timestamp())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Humidity_temp(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	humidity = db.Column(db.Integer)
	temp = db.Column(db.Integer)
	timestamp = db.Column(db.Integer ,index=True, default=datetime.utcnow().timestamp())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
