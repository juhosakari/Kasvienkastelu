from app import app
from flask import
from flask_login import current_user, logout_user, login_user, login_required
from app.models import User

@app.route('/')
@app.route('/change_user', methods=['POST'])
def change_user(user):
	if request.method == 'POST':
		if current_user.is_authenticated:
			logout_user()
		user = User.query.filter_by(name=user).first()
		login_user(user, remember=True)
		return redirect(url_for('index', user=user))
	else:
		return url_for('change_user')

@app.route('/index/<user>')
@login_required
def index(user):
	return render_template('index.html', user=user)

@app.route('/autowater')
def autowater():
	return redirect(url_for('index'))

@app.route('/autofertilize')
def autofertilize():
	#todo
	return redirect(url_for('index'))

@app.route('/settings')
def settings():
	return render_template('settings.html')
