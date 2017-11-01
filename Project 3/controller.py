from __future__ import print_function  # use python 3 syntax but make it compatible with python 2
from __future__ import division  # ''

import time  # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers
import grovepi


BP = brickpi3.BrickPi3()  # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)  # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.LIGHT)  # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.
ultrasonic_sensor_port = 4

# gets the distance value of the sensor
def getDistance():
    try:
        return grovepi.ultrasonicRead(ultrasonic_sensor_port)
    except brickpi3.SensorError:
        print('Error: Distance Sensor')

# checks if button is pressed
def getTouch():
    try:
        return BP.get_sensor(BP.PORT_1)
    except brickpi3.SensorError:
        print('Error: Touch Sensor')

    # sets the power for the given motor
def setMotor(motor, power):
    if motor == 1 or motor == 'a':
        BP.set_motor_power(BP.PORT_A, power)
    elif motor == 2 or motor == 'b':
        BP.set_motor_power(BP.PORT_B, power)
    elif motor == 3 or motor == 'c':
        BP.set_motor_power(BP.PORT_C, power)
    elif motor == 4 or motor == 'd':
        BP.set_motor_power(BP.PORT_D, power)
    else:
        print('Not a valid motor')

    # returns the orientation of the motor
def getMotor(motor):
    try:
        if motor == 1 or motor == 'a':
            return BP.get_motor_encoder(BP.PORT_A)
        elif motor == 2 or motor == 'b':
            return BP.get_motor_encoder(BP.PORT_B)
        elif motor == 3 or motor == 'c':
            return BP.get_motor_encoder(BP.PORT_C)
        elif motor == 4 or motor == 'd':
            return BP.get_motor_encoder(BP.PORT_D)
        else:
            print('Not a valid motor')
    except IOError as error:
        print(error)

def data():
    print("Sensor: %6d Motor A: %6d  B: %6d  C: %6d  D: %6d" \
          % (grovepi.ultrasonicRead(ultrasonic_sensor_port), \
             BP.get_motor_encoder(BP.PORT_A), \
             BP.get_motor_encoder(BP.PORT_B), \
             BP.get_motor_encoder(BP.PORT_C), \
             BP.get_motor_encoder(BP.PORT_D)))

def stop():
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
    BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))

    BP.reset_all()

a = 'a'
b = 'b'
c = 'c'
d = 'd'

def left():
    setMotor(a, -30)
    setMotor(d, 30)
    time.sleep(1.10)
    setMotor(a, 0)
    setMotor(d, 0)

def right():
    setMotor(a, 30)
    setMotor(d, -30)
    time.sleep(1.10)
    setMotor(a, 0)
    setMotor(d, 0)

def straight(t):
    setMotor(a, 30)
    setMotor(d, 0)
    time.sleep(t)
    setMotor(a, 0)
    setMotor(d, 0)

def stop():
    setMotor(a, 0)
    setMotor(d, 0)

def userControl():
    go = input('How to move:')
    while True:
        if go == 'r':
            right()
        elif go == 'l':
            left()
        elif go == 'm':
            setMotor(1, 20)
            setMotor(4, 20)
        elif go == 's':
            setMotor(1, 0)
            setMotor(4, 0)
        elif go == 'b':
            setMotor(1,-10)
            setMotor(4,-10)
        elif go == 'stop':
            break


def avoidObstacle():
    state = 'moving'
    x = 0
    while True:
        if state == 'moving':
            moveDistance(5)
            time(0.1)
            if getDistance() < 15:
                state == 'state1'
        elif state == 'state1':
            left()
            moveDistance(10)
            x += 1
            right()
            if getDistance() > 30:
                left()
                moveDistance(10)
                x += 1
                right()
                state == 'state2'
                moveDistance(30)
                right()
        elif state == 'state2':
            if getDistance() < 30:
                left()
                moveDistance(20)
                right()
            else:
                left()
                moveDistance(20)
                right()
                state == 'state3'
        elif state == 'state3':
            for n in range(x):
                moveDistance(20)
                time.sleep(.1)
            left()
            moveDistance(50)
            break

def moveSpeed(cmps):
    pd = (getMotor(1) + getMotor(4))/2
    pt = time.time()
    #convert cm to angle
    circumference = 8
    goal = cmps * 360 / circumference
    speed = 0
    power = 0
    adder = 0
    max_power = 40
    while True:
        d = (getMotor(1) + getMotor(4)) / 2
        t = time.time()
        speed = (d - pd)/(t - pt)/(360 * circumference)

        adder = goal - speed
        power += adder
        if power > max_power:
            power = max_power
        elif power < 0:
            power = 0
        pd = d
        pt = t


def moveDistance(cm):
    pd = (getMotor(1) + getMotor(4))/2
    pt = time.time()
    #convert cm to angle
    circumference = 8
    goal = pd + cm * 360 / circumference
    speed = 0
    power = 0
    adder = 0
    max_power = 40
    while True:
        d = (getMotor(1) + getMotor(4)) / 2
        t = time.time()
        speed = (d - pd)/(t - pt)/(360 * circumference)

        adder = (goal - d) / 1000 - speed
        power += adder
        if power > max_power:
            power = max_power
        elif power < 0:
            power = 0
        if abs(speed) < 10 and abs(d - pd) < 10:
            setMotor(1,0)
            setMotor(4,0)
            break
        pd = d
        pt = t



def ramp():
    pass

try:
    while True:
        do = input('What would you like to do')
        if do == 'stop':
            stop()
            break
        elif do == 'avoid':
            avoidObstacle()
        elif do == 'ramp':
            ramp()



except KeyboardInterrupt:
    pass

stop()