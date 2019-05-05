from app import db
from app.models import User, Pics, Water, Humidity_temp
from flask_login import current_user
import RPi.GPIO as GPIO
from datetime import datetime
from picamera import PiCamera
from time import sleep, sleep
import DHT22
import pigpio
from gpiozero import Servo

GPIO.setmode(GPIO.BCM)

def get_status(pin):
	GPIO.setup(pin, GPIO.IN) 
	return GPIO.input(pin)

def water(pump_pin, servo, sensor_pin, user):
	if GPIO.input(sensor_pin):
		servo.mid()
		sleep(0.5)
		if servo_turn == "right":
			servo.min()
		else:
			servo.max()
		GPIO.output(pump_pin, GPIO.LOW)
		sleep(0.5)
		GPIO.output(pump_pin, GPIO.HIGH)
		sleep(2)#sleep(user.water_amount)
		GPIO.output(pump_pin, GPIO.LOW)
		water = Water(user=user ,amount_watered=user.water_amount, timestamp=datetime.utcnow().timestamp())
		db.session.add(water)
		db.session.commit()


def temphum(user, datapin):
	try:
		last_measure = Humidity_temp.query.order_by(Humidity_temp.timestamp.desc()).first()
	except:
		last_measure = None
	if last_measure == None or datetime.utcnow().timestamp() - last_measure.timestamp  >= user.humidity_temp_i*60:
		pi=pigpio.pi()
		s=DHT22.sensor(pi,datapin)
		s.trigger()
		sleep(2)
		h=s.humidity()
		t=s.temperature()
		s.cancel()
		sleep(0.2)
		pi.stop()
		measure = Humidity_temp(humidity=h, temp=t, timestamp=datetime.utcnow().timestamp())
		db.session.add(measure)
		db.session.commit()

def snap(user):
	try:
		last_snap = Pics.query.order_by(Pics.date.desc()).first()
	except:
		last_snap = None
	if last_snap == None or datetime.utcnow().timestamp() - last_snap.date  >= user.snap_i*60:
		print("yks")
		pic = Pics(path="random", date=datetime.utcnow().timestamp())
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
	SERVO_PIN_1			= 5
	SERVO_PIN_2			= 6
	WATER_SENSOR_1		= 21
	WATER_SENSOR_2		= 18
	HUMIDITY_TEMP		= 4

	GPIO.setup([SERVO_PIN_2, SERVO_PIN_1, PUMP_WATER, PUMP_FERTILIZER], GPIO.OUT)
	GPIO.setup([WATER_SENSOR_1, WATER_SENSOR_2], GPIO.IN)

	maxturn = (2.0+0.45)/1000
	minturn = (1.0-0.45)/1000
	servo1 = Servo(SERVO_PIN_1, max_pulse_width=maxturn, min_pulse_width=minturn)
	servo2 = Servo(SERVO_PIN_2, max_pulse_width=maxturn, min_pulse_width=minturn)

	users = User.query.all()

	try:
		while True:
			for user in users:
				if user.autowater:
					if user.name == 'kayttaja1' or user.name == 'kayttaja3':
						pump_pin = PUMP_FERTILIZER
						if user.name == 'kayttaja1':
							servo_turn = "right"
						else:
							servo_turn = "left"
						water(pump_pin, servo1, WATER_SENSOR_2, servo_turn, user)
						#servo_turn= direction in which servo will turn(right/left)
					else:
						pump_pin = PUMP_WATER
						if user.name == 'kayttaja2':
							servo_turn = "right"
						else:
							servo_turn = "left"
						water(pump_pin, servo2, WATER_SENSOR_1, servo_turn, user)
			temphum(user, HUMIDITY_TEMP)
			snap(user)
			sleep(1)
	except KeyboardInterrupt:
		GPIO.cleanup()

if __name__ == '__main__':
	main()
