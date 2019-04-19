from app import db
from app.models import User, Pics, Water, Humidity_temp
from flask_login import current_user
import RPi.GPIO as GPIO
import datetime
from picamera import PiCamera
import time
import DHT22
import pigpio

GPIO.setmode(GPIO.BCM)

def get_status(pin):
    GPIO.setup(pin, GPIO.IN) 
    return GPIO.input(pin)

def water(pump_pin, servo_pin, sensor_pin, user):
	if GPIO.input(sensor_pin):
		GPIO.output(pump_pin, GPIO.HIGH)
		time.sleep(user.water_amount)
		GPIO.output(pump_pin, GPIO.LOW)
		water = Humidity_temp(amount_watered=user.water_amount)
    	db.session.add(measure)
    	db.session.commit()


def temphum(user):
	last_measure = user.humidity_temp.order_by(Humidity_temp.timestamp.desc()).first()
	if last_measure == None or datetime.utcnow -last_measure.timestamp >= user.humidity_temp_i:
		pi=pigpio.pi()
		datapin=4
    	s=DHT22.sensor(pi,datapin)
    	s.trigger()
    	sleep(2)
    	t=s.humidity()
    	h=s.temperature()
    	s.cancel
    	pi.stop()
    	measure = Humidity_temp(humidity=h, temp=t)
    	db.session.add(measure)
    	db.session.commit()

def snap(user):
	last_snap = user.pics.order_by(Pics.timestamp.desc()).first()
	if last_snap == None or datetime.utcnow -last_snap.timestamp >= user.snap_i:
		pic = Pics(author=current_user, post_pic_path="random")
		y = Pics.query.order_by(Pics.timestamp.desc()).first()
		filename = "post" + str(y.id) + ".png"
    	with PiCamera() as camera:
        	camera.capture('app/static/'+ filename)
        pic.path = filename
        db.session.add(pic)
        db.session.commit()

def main():
	#Raspberry pi gpio pins
	PUMP_WATER = 0
	PUMP_FERTILIZER = 0
	SERVO_1 = 0
	SERVO_2 = 0
	WATER_SENSOR = 0
	HUMIDITY_TEMP = 0

	GPIO.setup([PUMP_WATER, PUMP_FERTILIZER, SERVO_2, SERVO_1, WATER_SENSOR], GPIO.OUT)
	GPIO.setup(WATER_SENSOR, GPIO.OUT)

	users = User.query.all()

	try:
		while True:
			users = get_values()
			for user in users:
				if user.name == 'kayttaja1' or user.name == 'kayttaja3':
					servo_pin = SERVO_1
					pump_pin = PUMP_FERTILIZER
				else:
					servo_pin = SERVO_2
					pump_pin = PUMP_WATER
				water(pump_pin, servo_pin, WATER_SENSOR, user)
			temphum(user)
			snap(user)
			#time.sleep(1)
	except KeyboardInterrupt:
		GPIO.cleanup()

main()