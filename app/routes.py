from app import app, db
from flask import redirect, url_for, render_template, request
from flask_login import current_user, logout_user, login_user, login_required
from app.models import User, Humidity_temp, Water, Pics
import datetime
import socket
import os
import psutil

import pdb

def autowater(request):
	running = False
	if request:
		for process in psutil.process_iter():
			try:
				if process.cmdline()[1] == 'autowater.py':
					running = True
			except:
				pass
		if not running:
			current_user.autowater = True
			os.system("python3.4 auto_water.py&")
		else:
			current_user.autowater = True

	else:
		current_user.autowater = False
		users = User.query.all()
		for user in users:
			if user.autowater == True:
				return 0
    	os.system("pkill -f water.py")

@app.route('/')
@app.route('/change_user', methods=['POST', 'GET'])
def change_user():
	logout_user()
	if request.method == 'POST':
		user = User.query.filter_by(name=request.form['user_button']).first()
		login_user(user, remember=True)
		return redirect(url_for('index', user=current_user.name))
	else:
		return render_template('change_user.html', user=current_user)

@app.route('/index/<user>')
@login_required
def index(user):
	#pdb.set_trace()
	last_measure = Humidity_temp.query.order_by(Humidity_temp.timestamp.desc()).first()
	last_water = current_user.water.order_by(Water.timestamp.desc()).first()
	last_pic = Pics.query.order_by(Pics.date.desc()).first()
	print(last_measure, last_water, last_pic)

	if last_measure is None or last_water is None:
		return render_template('index.html', user=current_user, 
						   time=datetime.datetime.now().strftime("%H:%M %d.%m.%Y"),
						   temphum_timestamp="None",
						   water_timestamp="None",
						   temp="None",
						   humidity="None",
						   water_amount="None",
						   pic_path="lammas.jpg",
						   pic_timestamp="None"
						   )

	return render_template('index.html', 
						   user=current_user, 
						   time=datetime.datetime.now().strftime("%H:%M %d.%m.%Y"),
						   temphum_timestamp=print(datetime.utcfromtimestamp(last_measure.timestamp).strftime('%Y-%m-%d %H:%M')),
						   water_timestamp=print(datetime.utcfromtimestamp(last_water.timestamp).strftime('%Y-%m-%d %H:%M')),
						   temp=round(last_measure.temp, 1),
						   humidity=round(last_measure.humidity, 1),
						   water_amount=last_water.amount_watered,
						   pic_path=last_pic.path,
						   pic_timestamp=print(datetime.utcfromtimestamp(last_pic.date).strftime('%Y-%m-%d %H:%M'))
						   )

#Kannattaako autowater laittaa linkiksi vai asetuksiin yhdeksi formin osaksi?
@app.route('/settings', methods=['POST', 'GET'])
@login_required
def settings():
	error = False
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s.connect(('8.8.8.8',80))
	if s.getsockname()[0] == request.remote_addr:
		if request.method == 'POST':
			try:
				users = User.query.all()
				for user in users:
					user.snap_i = int(request.form['snap_i']) #Muutetaan minuutit sekunneiksi
					user.humidity_temp_i = int(request.form['humidity_temp_i'])
				current_user.water_amount = int(request.form['water_amount'])
				#if int(request.form['auto']) != current_user.autowater:
				autowater(int(request.form['auto']))
			except:
				error = "Jokin arvoista on väärin. Muista että vain kokonaisluvut kelpaavat!"
				return render_template('settings.html', current_user=current_user, error=error)
				
			db.session.commit()
			return redirect(url_for('index', user=current_user.name))
		return render_template('settings.html', user=current_user, error=error)
	return redirect(url_for('index', user=current_user.name))
