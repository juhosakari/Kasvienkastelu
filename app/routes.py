from app import app, db
from flask import redirect, url_for, render_template, request
from flask_login import current_user, logout_user, login_user, login_required
from app.models import User, Humidity_temp, Water, Pics
import datetime

import pdb

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
	print("Current user: ", current_user)
	
	last_measure = current_user.humidity_temp.order_by(Humidity_temp.timestamp.desc()).first()
	last_water = current_user.water.order_by(Water.timestamp.desc()).first()
	last_pic = current_user.pics.order_by(Pics.date.desc()).first()

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

@app.route('/autowater')
def autowater():
	'''
	running = False
    if toggle == "ON":
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_water.py':
                    running = True
                    break
            except:
                pass
        if not running:
            os.system("python3.4 auto_water.py&")
    else:
        templateData = template(text = "Auto Watering Off")
		os.system("pkill -f water.py")
	'''
	return redirect(url_for('index', user=current_user))



@app.route('/autofertilize') 
def autofertilize():
	#todo
	return redirect(url_for('index', user=current_use))

@app.route('/settings', methods=['POST', 'GET'])
@login_required
def settings():
	error = False
	if request.method == 'POST':
		#user = User.query.filter_by(name=current_user.name).first()
		try:
			current_user.snap_i = int(request.form['snap_i'])
			current_user.water_amount = int(request.form['water_amount'])
			#current_user.autowater = int(request.form['autowater'])
			current_user.humidity_temp_i = int(request.form['humidity_temp_i'])
		except:
			error = "Jokin arvoista on väärin. Muista että vain kokonaisluvut kelpaavat!"
			return render_template('settings.html', current_user=current_user, error=error)
		db.session.commit()
		return redirect(url_for('index', user=current_user.name))
	return render_template('settings.html', user=current_user, error=error)
