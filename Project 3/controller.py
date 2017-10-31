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

def getLight():
    try:
        return BP.get_sensor(BP.PORT_2)
    except brickpi3.SensorError:
        print('Error: Light Sensor')

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

class PID(object):
    """A generic PID loop controller which can be inherited and used in other control algorithms"""

    def __init__(self, startingError):
        """Return a instance of a un tuned PID controller"""
        self._p = 1
        self._i = 0
        self._d = 0
        self._esum = 0 #Error sum for integral term
        self._le =startingError    #Last error value

    def calculate(self, error, dt):
        """Calculates the output of the PID controller"""
        self._esum += error*dt
        dError = (error - self._le)/dt
        u = self._p*error + self._i*self._esum + self._d *dError
        self._le = error
        return u


    def reset(self, startingError):
        """Resets the integral sum and the last error value"""
        self._esum = 0
        self._le = startingError
    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, value):
        self._p = value

    @property
    def i(self):
        return self._i

    @i.setter
    def i(self, value):
        self._i = value

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, value):
        self._d = value