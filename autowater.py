def get_values():
	users = User.query.all()
	return users

def main():
	from app import db
	from app.models import User, Pics, Water, Fertilize, Humidity_temp
	import RPi.GPIO as GPIO
	import datetime
	import time
	#Raspberry pi gpio pins
	PUMP_1 = 0
	PUMP_2 = 0
	SERVO_1 = 0
	SERVO_2 = 0
	HUMIDITY_TEMP = 0

	while True:
		users = get_values()


get_values()