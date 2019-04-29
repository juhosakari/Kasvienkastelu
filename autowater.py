from app import db
from app.models import User, Pics, Water, Humidity_temp
from flask_login import current_user
import RPi.GPIO as GPIO
from datetime import datetime
from picamera import PiCamera
from time import sleep
from time import time # time.time() = unix time (in millisecond)
#import DHT22
#import pigpio

GPIO.setmode(GPIO.BCM)

def get_status(pin):
	GPIO.setup(pin, GPIO.IN) 
	return GPIO.input(pin)

def water(pump_pin, servo_pin, sensor_pin, user):
	if GPIO.input(sensor_pin):
		#print(GPIO.input(sensor_pin))
		GPIO.output(pump_pin, GPIO.LOW)
		sleep(1)
		GPIO.output(pump_pin, GPIO.HIGH)
		sleep(2)#user.water_amount
		GPIO.output(pump_pin, GPIO.LOW)
		water = Water(user=user ,amount_watered=user.water_amount)
		db.session.add(water)
		db.session.commit()


def temphum(user, datapin):
	try:
		last_measure = user.humidity_temp.order_by(Humidity_temp.timestamp.desc()).first()
	except:
		last_measure = None
	if last_measure == None or last_measure.timestamp - datetime.utcnow().timestamp() >= user.humidity_temp_i*60:
		pi=pigpio.pi()
		s=DHT22.sensor(pi,datapin)
		s.trigger()
		sleep(2)
		t=s.humidity()
		h=s.temperature()
		s.cancel()
		sleep(0.2)
		pi.stop()
		measure = Humidity_temp(humidity=h, temp=t)
		db.session.add(measure)
		db.session.commit()

def snap(user):
	try:
		last_snap = user.pics.order_by(Pics.timestamp.desc()).first()
	except:
		last_snap = None
	if last_snap == None or last_measure.date - datetime.utcnow().timestamp() >= user.snap_i*60:
		pic = Pics(user=user, path="random")
		try:
			y = Pics.query.order_by(Pics.date.desc()).first()
			filename = "post" + str(y.id) + ".png"
		except:
			filename = "post.png"
		with PiCamera() as camera:
			camera.capture('app/static/'+ filename)
		pic.path = filename
		db.session.add(pic)
		db.session.commit()

def main():
	#Raspberry pi gpio pins
	PUMP_WATER		= 19
	PUMP_FERTILIZER		= 26
	SERVO_1			= 5
	SERVO_2			= 6
	WATER_SENSOR_1		= 21
	WATER_SENSOR_2		= 18
	HUMIDITY_TEMP		= 4


	GPIO.setup(PUMP_WATER,GPIO.OUT)
	GPIO.setup(PUMP_FERTILIZER, GPIO.OUT)
	GPIO.setup([SERVO_2, SERVO_1], GPIO.OUT)
	GPIO.setup(WATER_SENSOR_1, GPIO.IN)
	GPIO.setup(WATER_SENSOR_2, GPIO.IN)

	users = User.query.all()

	try:
		while True:
			for user in users:
				if user.name == 'kayttaja1' or user.name == 'kayttaja3':
					#print("yks")
					servo_pin = SERVO_1
					pump_pin = PUMP_FERTILIZER
					water(pump_pin, servo_pin, WATER_SENSOR_2, user)
				else:
					servo_pin = SERVO_2
					pump_pin = PUMP_WATER
					water(pump_pin, servo_pin, WATER_SENSOR_1, user)
			temphum(user, HUMIDITY_TEMP)
			snap(user)
			sleep(1)
	except KeyboardInterrupt:
		GPIO.cleanup()

if __name__ == '__main__':
	main()
