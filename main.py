from flask import Flask, render_template
from gpiozero import Motor
from time import sleep
from threading import Event, Thread

import RPi.GPIO as GPIO

app = Flask(__name__)

motot1_in1 = 24
motot1_in2 = 23
en1 = 25
motor2_in1 = 20
mototr2_in2 = 16
en2 = 21
steer_in1 = 22
steer_in2 = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(motot1_in1,GPIO.OUT)
GPIO.setup(motot1_in2,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)

GPIO.setup(motor2_in1,GPIO.OUT)
GPIO.setup(mototr2_in2,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)

GPIO.setup(steer_in1,GPIO.OUT)
GPIO.setup(steer_in2,GPIO.OUT)

GPIO.output(motot1_in1,GPIO.LOW)
GPIO.output(motot1_in2,GPIO.LOW)
GPIO.output(motor2_in1,GPIO.LOW)
GPIO.output(mototr2_in2,GPIO.LOW)
GPIO.output(steer_in1,GPIO.LOW)
GPIO.output(steer_in2,GPIO.LOW)

p=GPIO.PWM(en1,1000)
p2=GPIO.PWM(en2,1000)
p.start(25)
p2.start(25)

global state

state = ""

# added this while loop for capturing the timing of button click and to make sure that it always stay same state
def motor_job():

    while True:
        if state == "forward":
        
            # motor back and front
            GPIO.output(motot1_in1,GPIO.HIGH)
            GPIO.output(motot1_in2,GPIO.LOW)
            GPIO.output(motor2_in1,GPIO.HIGH)
            GPIO.output(mototr2_in2,GPIO.LOW)

        elif state == "stop":

            # motor back and front
            GPIO.output(motot1_in1,GPIO.LOW)
            GPIO.output(motot1_in2,GPIO.LOW)
            GPIO.output(motor2_in1,GPIO.LOW)
            GPIO.output(mototr2_in2,GPIO.LOW)

        elif state == "backward":

            # motor back and front
            GPIO.output(motot1_in1,GPIO.LOW)
            GPIO.output(motot1_in2,GPIO.HIGH)
            GPIO.output(motor2_in1,GPIO.LOW)
            GPIO.output(mototr2_in2,GPIO.HIGH)

        elif state == "left":

            # motor back and front
            GPIO.output(motot1_in1,GPIO.HIGH)
            GPIO.output(motot1_in2,GPIO.LOW)
            GPIO.output(motor2_in1,GPIO.HIGH)
            GPIO.output(mototr2_in2,GPIO.LOW)

            GPIO.output(steer_in1,GPIO.LOW)
            GPIO.output(steer_in2,GPIO.HIGH)

        elif state == "right":

            # motor back and front
            GPIO.output(motot1_in1,GPIO.HIGH)
            GPIO.output(motot1_in2,GPIO.LOW)
            GPIO.output(motor2_in1,GPIO.HIGH)
            GPIO.output(mototr2_in2,GPIO.LOW)

            GPIO.output(steer_in1,GPIO.HIGH)
            GPIO.output(steer_in2,GPIO.LOW)

        elif state == "straight":

            # motor back and front
            GPIO.output(motot1_in1,GPIO.LOW)
            GPIO.output(motot1_in2,GPIO.LOW)
            GPIO.output(motor2_in1,GPIO.LOW)
            GPIO.output(mototr2_in2,GPIO.LOW)

            GPIO.output(steer_in1,GPIO.LOW)
            GPIO.output(steer_in2,GPIO.LOW)

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
