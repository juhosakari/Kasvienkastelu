from app import app, db
from flask import redirect, url_for, render_template, request
from flask_login import current_user, logout_user, login_user, login_required
from app.models import User, Humidity_temp, Water, Pics
import datetime
import socket
import os

import pdb

def autowater():
	if current_user.autowater == False:
		os.system("python3 autowater.py&")
		current_user.autowater = True
	else:
		os.system("pkill -f autowater.py")
		current_user.autowater = False
	return redirect(url_for('settings', user=current_user))

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
	last_measure = current_user.humidity_temp.order_by(Humidity_temp.timestamp.desc()).first()
	last_water = current_user.water.order_by(Water.timestamp.desc()).first()
	last_pic = Pics.query.order_by(Pics.date.desc()).first()

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
						   temphum_timestamp=last_measure.timestamp,
						   water_timestamp=last_water.timestamp,
						   temp=last_measure.temp,
						   humidity=last_measure.humidity,
						   water_amount=last_water.water_amount,
						   pic_path=last_pic.path,
						   pic_timestamp=last_pic.timestamp
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
				if int(request.form['auto']) != current_user.autowater:
					autowater()
			except:
				error = "Jokin arvoista on väärin. Muista että vain kokonaisluvut kelpaavat!"
				return render_template('settings.html', current_user=current_user, error=error)
				
			db.session.commit()
			return redirect(url_for('index', user=current_user.name))
		return render_template('settings.html', user=current_user, error=error)
	return redirect(url_for('index', user=current_user.name))
