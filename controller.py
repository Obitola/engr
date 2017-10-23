from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi

class SensorReader():
    BP = brickpi3.BrickPi3()  # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
    BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)  # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.
    BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.LIGHT)  # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.
    ultrasonic_sensor_port = 4
    def __init__(self):
        pass

    #gets the distance value of the sensor
    def getDistance(self):
        return grovepi.ultrasonicRead(self.ultrasonic_sensor_port)

    #checks if button is pressed
    def getTouch(self):
        try:
            return self.BP.get_sensor(self.BP.PORT_1)
        except brickpi3.SensorError:
            pass

    def getLight(self):
        try:
            return self.BP.get_sensor(self.BP.PORT_2)
        except brickpi3.SensorError:
            pass

    #sets the power for the given motor
    def setMotor(self,motor,power):
        if motor == 1 or motor == 'a':
            self.BP.set_motor_power(self.BP.PORT_A, power)
        elif motor == 2 or motor == 'b':
            self.BP.set_motor_power(self.BP.PORT_B, power)
        elif motor == 3 or motor == 'c':
            self.BP.set_motor_power(self.BP.PORT_C, power)
        elif motor == 4 or motor == 'd':
            self.BP.set_motor_power(self.BP.PORT_D, power)
        else:
            print('Not a valid motor')

    #returns the orientation of the motor
    def getMotor(self,motor):
        try:
            if motor == 1 or motor == 'a':
                return self.BP.get_motor_encoder(self.BP.PORT_A)
            elif motor == 2 or motor == 'b':
                return self.BP.get_motor_encoder(self.BP.PORT_B)
            elif motor == 3 or motor == 'c':
                return self.BP.get_motor_encoder(self.BP.PORT_C)
            elif motor == 4 or motor == 'd':
                return self.BP.get_motor_encoder(self.BP.PORT_D)
            else:
                print('Not a valid motor')
        except IOError as error:
            print(error)