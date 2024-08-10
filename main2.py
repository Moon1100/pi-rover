from flask import Flask, render_template
from gpiozero import Motor
from time import sleep
from threading import Event, Thread

import RPi.GPIO as GPIO

app = Flask(__name__)



GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

# Define the motor with forward and backward pins
# motor = Motor(forward=17, backward=18)
# steer = Motor(forward=22, backward=23)

# Flag to indicate if motor is currently running
motor_running = Event()
# steer_turned = False


global state

state = ""

# added this while loop for capturing the timing of button click and to make sure that it always stay same state
def motor_job():

        while not motor_running.is_set():
         if state == "forward":
          GPIO.output(17,GPIO.HIGH)
          GPIO.output(18,GPIO.LOW)
         elif state == "stop":
          GPIO.output(17,GPIO.LOW)
          GPIO.output(18,GPIO.LOW)
         elif state == "backward":
          GPIO.output(17,GPIO.LOW)
          GPIO.output(18,GPIO.HIGH)
         elif state == "left":
          GPIO.output(17,GPIO.HIGH)
          GPIO.output(18,GPIO.LOW)
          GPIO.output(23,GPIO.HIGH)
          GPIO.output(22,GPIO.LOW)
         elif state == "right":
          GPIO.output(17,GPIO.HIGH)
          GPIO.output(18,GPIO.LOW)
          GPIO.output(22,GPIO.HIGH)
          GPIO.output(23,GPIO.LOW)
         elif state == "straight":
          GPIO.output(17,GPIO.LOW)
          GPIO.output(18,GPIO.LOW)
          GPIO.output(22,GPIO.LOW)
          GPIO.output(23,GPIO.LOW)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forward')
def forward():
    # global motor_running
    # motor_running = True
    # motor.forward()
    global state
    state = "forward"

    return 'Motor moved forward'

@app.route('/backward')
def backward():
    #global steer_turned
    #steer_turned = False
    #steer.stop()
    #global motor_running
    #motor_running = True
    #motor.backward()
    global state
    state = "backward"

    return 'Motor moved backward'

@app.route('/left')
def left():
    #global steer_turned
    #steer_turned = True
    #steer.backward()
    #global motor_running
    #motor_running = True
    #motor.forward()
    global state
    state = "left"

    return 'steer moved left'

@app.route('/right')
def right():
    #global steer_turned
    #steer_turned = True
    #steer.forward()
    #global motor_running
    #motor_running = True
    #motor.forward()
    global state
    state = "right"

    return 'steer moved right'

@app.route('/stop')
def stop():

    # global motor_running
    # motor_running = False
    # motor.stop()
    global state
    state = "stop"

    return 'Motor stopped'


@app.route('/straight')
def straight():
    #global steer_turned
    #steer_turned = False
    #steer.stop()
    #global motor_running
    #motor_running = False
    #motor.stop()
    global state
    state = "straight"

    return 'Steer stopped'


@app.route('/status')
def status():
    return 'Motor is running' if motor_running else 'Motor is stopped'


if __name__ == '__main__':
    # Added Thread from running while loop(motor_job) concurrent with app run
    Thread(target=motor_job).start()
    app.run(debug=True, host='0.0.0.0')