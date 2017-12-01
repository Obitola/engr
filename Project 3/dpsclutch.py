from __future__ import print_function  # use python 3 syntax but make it compatible with python 2
from __future__ import division  # ''

import time  # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers
# import grovepi
import MasterFunct as pmad
import smbus
from math import pi

BP = brickpi3.BrickPi3()  # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)  # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_LIGHT_ON)
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.NXT_LIGHT_ON)

ultrasonic_sensor_port = 4
white = 2500
black = 2800
radius = 4


# A generic PID loop controller for control algorithms
class PID(object):
    # Return a instance of a un tuned PID controller
    def __init__(self, startingError):
        self._p = 0.9
        self._i = 0.05
        self._d = 0.5
        self._esum = 0  # Error sum for integral term
        self._le = startingError  # Last error value

    # Calculates the output of the PID controller
    def calculate(self, error, dt):
        self._esum += error * dt
        dError = (error - self._le) / dt
        u = self._p * error + self._i * self._esum + self._d * dError
        self._le = error
        return u

    # Resets the integral sum and the last error value
    def reset(self, startingError):
        self._esum = 0
        self._le = startingError


class mcms(object):
    def __init__(self):
        self.steer = 0
        self.speed = 0

    def move_distance(self, distance, speed):
        self.steer = 0
        self.set_speed(speed)
        start_time = time.time()
        total_time = abs(distance / speed)
        while time.time() - start_time < total_time:
            self.update()
        self.stop()

    def update(self):
        self.set_speed(self.speed)

    def get_claw_position(self):
        return self.get_motor(3)

    # gets the distance value of the sensor
    def get_ultrasonic_distance(self):
        try:
            return grovepi.ultrasonicRead(ultrasonic_sensor_port)
        except brickpi3.SensorError:
            print('Error: Distance Sensor')

    # checks if button is pressed
    def get_touch(self):
        try:
            return BP.get_sensor(BP.PORT_1)
        except brickpi3.SensorError:
            print('Error: Touch Sensor')
            # sets the power for the given motor

    def get_nxt_light(self):
        try:
            return BP.get_sensor(BP.PORT_2)
        except brickpi3.SensorError:
            print('Error: Light Sensor')

    def get_hall_sensor(self):
        try:
            return BP.get_sensor(BP.PORT_4)
        except brickpi3.SensorError:
            print('Error: Hall Sensor')

    def set_dps(self, motor, dps):
        try:
            if motor == 1:
                BP.set_motor_dps(BP.PORT_A, dps)
            elif motor == 2:
                BP.set_motor_dps(BP.PORT_B, dps)
            elif motor == 3:
                BP.set_motor_dps(BP.PORT_C, dps)
            elif motor == 4:
                BP.set_motor_dps(BP.PORT_D, dps)
        except:
            print('Error: DPS Motor Error')

    def set_motor(self, motor, power):
        try:
            BP.set_motor_power(BP.PORT_C, power)
        except:
            print('error')
    
    # returns the orientation of the motor
    def get_motor(self, motor):
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

    def data(self):
        print("Speed: %3d Light: %6d  Hall: %6d  Steer: %3d " \
              % (self.speed, \
                 self.get_nxt_light(), \
                 self.get_hall_sensor(), \
                 self.steer))

    def shutdown(self):
        BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
        BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
        BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
        BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))

        BP.reset_all()

    def set_speed(self, speed):
        self.speed = speed
        dps = speed * 360 / (2 * pi * radius)
        dps_right = dps * (1 + self.steer)
        dps_left = dps * (1 - self.steer)
        self.set_dps(1, dps_right)
        self.set_dps(4, dps_left)

    def straight(self):
        self.steer = 0

    def set_steer(self, direction, amount):
        if direction == 'right':
            self.steer = amount
        elif direction == 'left':
            self.steer = -amount
        if self.steer > 2:
            self.steer = 2
        elif self.steer < -2:
            self.steer = -2

    def stop(self):
        self.desired_speed = 0
        self.set_motor(1, 0)
        self.set_motor(4, 0)
        self.set_motor(2, 0)
        self.set_motor(3, 0)

    def open_claw(self):
        count = 1
        for x in range(36):
            snot.set_motor(3, 16)
            time.sleep(0.2)
            snot.set_motor(3, 0)
            time.sleep(0.1)

    def close_claw(self):
        for x in range(45):
            snot.set_motor(3, -25)
            time.sleep(0.3)
            snot.set_motor(3, 0)
            time.sleep(0.1)


snot = mcms()


def line_follow():
    snot.set_speed(-3)
    snot.update()
    while not snot.get_touch():
        snot.set_steer('left', (snot.get_nxt_light() - ((white + black - 250) / 2)) / 150)
        snot.data()
        snot.update()

def straight():
    while not snot.get_touch():
        snot.data()
    snot.set_speed(-3)
    snot.update()
    while not snot.get_touch():
        #snot.set_steer('left', (snot.get_nxt_light() - ((white + black - 250) / 2)) / 150)
        snot.data()
        snot.update()

def energy():
    pmad.startPowerTracking(45)
    snot.set_speed(-12)
    while pmad.getPowerStored() >= 100:
        snot.update()
    snot.stop()


def data():
    while True:
        snot.data()
        time.sleep(0.3)

def legit():
    at_beacon = False
    while not snot.get_touch():
        snot.data()
    snot.set_speed(-5)
    snot.update()
    while not at_beacon:
        snot.set_steer('right', -2 +(snot.get_nxt_light() - ((white + black + 1000) / 2)) / 225)
        snot.data()
        snot.update()



try:
    # todo: implement mcms push button controls
    # todo: implement line following control
    go = 9
    while True:
        try:
            go = int(input('what would you like to do: '))
        except:
            print('Please input an integer')
        if go == 1:
            legit()
        elif go == 2:
            snot.close_claw()
        elif go == 6:
            snot.open_claw()
        elif go == 3:
            line_follow()
        elif go == 4:
            energy()
        elif go == 5:
            data()
        elif go == 7:
            straight()
        elif go == 0:
            break

except KeyboardInterrupt:
    pass

snot.shutdown()
