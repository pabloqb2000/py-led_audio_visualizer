from flask import Flask, render_template
import socket
from utils.to_leds import *
from colour import Color
import numpy as np

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/ledstrip.html")
def ledstrip():
	return render_template('ledstrip.html')

@app.route("/ledring.html")
def ledring():
	return render_template('ledring.html')

@app.route("/color/<colors>/<blit>/<odds>/<speed>")
def color_action(colors, blit, odds, speed):
	print(f"Colors: {colors} blit: {blit} odds: {odds} speed: {speed}")
	r,g,b = Color('#' + colors[:6]).rgb
	frame_to_leds(np.full((100, 3), (int(r*255), int(g*255), int(b*255))))
	return render_template('ledstrip.html')

'''@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	if deviceName == 'ledRed':
		actuator = ledRed
	if deviceName == 'ledYlw':
		actuator = ledYlw
	if deviceName == 'ledGrn':
		actuator = ledGrn
   
	if action == "on":
		GPIO.output(actuator, GPIO.HIGH)
	if action == "off":
		GPIO.output(actuator, GPIO.LOW)
		     
	ledRedSts = GPIO.input(ledRed)
	ledYlwSts = GPIO.input(ledYlw)
	ledGrnSts = GPIO.input(ledGrn)
   
	templateData = {
              'ledRed'  : ledRedSts,
              'ledYlw'  : ledYlwSts,
              'ledGrn'  : ledGrnSts,
	}
	return render_template('index.html', **templateData)'''

if __name__ == "__main__":
    ip = socket.gethostbyname(socket.gethostname())
    app.run(host='0.0.0.0', port=80, debug=True)