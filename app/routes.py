from app import app, db
from flask import redirect, url_for, render_template, request
from flask_login import current_user, logout_user, login_user, login_required
from app.models import User

@app.route('/')
@app.route('/change_user', methods=['POST', 'GET'])
def change_user():
	if request.method == 'POST':
		if current_user.is_authenticated:
			logout_user()
		user = User.query.filter_by(name=request.form['user_button']).first()
		login_user(user, remember=True)
		return redirect(url_for('index', user=current_user.name))
	else:
		return render_template('change_user.html')

@app.route('/index/<user>')
@login_required
def index(user):
	user_ = User.query.filter_by(name=user).first()
	print(user_.snap_i)
	return render_template('index.html', user=user)

@app.route('/autowater')
def autowater():
	return redirect(url_for('index'))

@app.route('/autofertilize')
def autofertilize():
	#todo
	return redirect(url_for('index'))

@app.route('/settings', methods=['POST', 'GET'])
@login_required
def settings():
	if request.method == 'POST':
		user = User.query.filter_by(name=current_user.name).first()
		try:
			user.snap_i = int(request.form['snap_i'])
		except:
			pass
		db.session.commit()
	return render_template('settings.html', user=current_user)
