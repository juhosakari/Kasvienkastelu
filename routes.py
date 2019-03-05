from flask import Flask, render_template, url_for
import socket
from flask_login import LoginManager

app = Flask(__name__)
login = LoginManager(app)


@app.route('/')
@app.route('/change_user')
def change_user():
	return render_template('change_user.html')

@app.route('/index/<user>')
def index(user):
	print(user)
	return render_template('index.html', user=user)

if __name__ == '__main__':
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s.connect(('8.8.8.8',80))
	print("server ip"+str(s.getsockname()[0])+":5001")
	app.run(host='0.0.0.0', port=5001, debug=True)