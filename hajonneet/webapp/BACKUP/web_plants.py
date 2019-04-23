from flask import Flask, render_template, redirect, url_for
#import psutil
import datetime
import water
import os
from readtemphum import temphum 

app = Flask(__name__)

def template(title = "HELLO!", text = ""):
    now = datetime.datetime.now()
    timeString = now
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : text
        }
    return templateDate

@app.route("/")
def hello():
    templateData = template()
    return render_template('main.html', **templateData)

@app.route("/last_watered")
def check_last_watered():
    templateData = template(text = water.get_last_watered())
    return render_template('main.html', **templateData)

@app.route("/sensor")
def action():
    status = water.get_status()
    message = ""
    if (status == 1):
        message = "Water me please!"
    else:
        message = "I'm a happy plant"

    templateData = template(text = message)
    return render_template('main.html', **templateData)

@app.route("/water")
def action2():
    #water.pump_on()
    #templateData = template(text = "Watered Once")
    templateData = template(text = "Not yet configured for watering")
    return render_template('main.html', **templateData)

@app.route('/plantwater')
def plant_water():
    t,h,m=temphum()
    templateData= template(text='Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(t,h) + '\n' +m)
    return render_template('main.html', **templateData)

"""
@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    running = False
    if toggle == "ON":
        templateData = template(text = "Auto Watering On")
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_water.py':
                    templateData = template(text = "Already running")
                    running = True
                    break
            except:
                pass
        if not running:
            os.system("python3.4 auto_water.py&")
    else:
        templateData = template(text = "Auto Watering Off")
os.system("pkill -f water.py")

    return render_template('main.html', **templateData)
"""
import socket

if __name__ == "__main__":
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    print("server ip "+str(s.getsockname()[0])+":5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
