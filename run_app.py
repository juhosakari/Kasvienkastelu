from app import app
import socket

if __name__ == '__main__':
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s.connect(('8.8.8.8',80))
	print("server ip"+str(s.getsockname()[0])+":5001")
	app.run(host='0.0.0.0', port=5001, debug=True)