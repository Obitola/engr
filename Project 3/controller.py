from __future__ import print_function  # use python 3 syntax but make it compatible with python 2
from __future__ import division  # ''

import time  # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers
#import grovepi
from MasterFunct import *
import smbus
from math import pi


BP = brickpi3.BrickPi3()  # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH) # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_LIGHT_ON)

ultrasonic_sensor_port = 4

#A generic PID loop controller for control algorithms
class PID(object):

    # Return a instance of a un tuned PID controller
    def __init__(self, startingError):
        self._p = 0.5
        self._i = 0.7
        self._d = 0.7
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
        self.previous_x = self.get_wheel_distance()
        self.previous_time = time.time() - 0.1
        self.current_speed = 0
        self.moving = False
        self.desired_speed = 0
        self.power = 0
        self.steer = 0
        self.pid = PID(0)
        self.power_list = [0,0,0,0,0]
        self.max_power = 200
        self.radius = 27
        self.desired_speed = 0

    def update(self):
        self.current_speed = (self.get_wheel_distance() - self.previous_x) / (time.time() - self.previous_time)
        error = self.desired_speed - self.current_speed
        if error < 0:
            self.pid.reset(error)

        #if self.moving:
        self.power += self.pid.calculate(error, time.time() - self.previous_time)#round((self.current_speed - self.desired_speed) / 2)
        self.set_motor(1,self.power * (1 + self.steer))
        self.set_motor(4,self.power * (1 - self.steer))
        print(self.desired_speed - self.current_speed)
        print(self.power_list)

        self.previous_x = self.get_wheel_distance()
        self.previous_time = time.time()
        time.sleep(0.1)

    def move_distance(self, distance, speed):
        self.update()
        start_time = time.time()
        total_time = distance / speed
        while time.time() - start_time < total_time:
            self.update()
        self.stop()

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

    def get_wheel_distance(self):
        return ((self.get_motor(1) + self.get_motor(4)) / 2) * (2 * pi * 3.5 / 360)

    def set_motor(self, motor, amount):
        self.power_list[motor] = amount

        if abs(self.power_list[1]) + abs(self.power_list[2]) + abs(self.power_list[3]) + abs(self.power_list[4])  > self.max_power:
            power_wheels = (self.max_power - abs(self.power_list[2]) - abs(self.power_list[3])) / (abs(self.power_list[1]) + abs(self.power_list[4]))
            BP.set_motor_power(BP.PORT_A, power_wheels * self.power_list[1])
            BP.set_motor_power(BP.PORT_B, self.power_list[2])
            BP.set_motor_power(BP.PORT_C, self.power_list[3])
            BP.set_motor_power(BP.PORT_D, power_wheels * self.power_list[4])

        else:
            BP.set_motor_power(BP.PORT_A, self.power_list[1])
            BP.set_motor_power(BP.PORT_B, self.power_list[2])
            BP.set_motor_power(BP.PORT_C, self.power_list[3])
            BP.set_motor_power(BP.PORT_D, self.power_list[4])

    # returns the orientation of the motor
    def get_motor(self, motor):
        try:
            if motor == 1 or motor == 'a':
                BP.get_motor_encoder(BP.PORT_A)
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
        print("Sensor: %6d Motor A: %6d  B: %6d  C: %6d  D: %6d" \
              % (grovepi.ultrasonicRead(ultrasonic_sensor_port), \
                 BP.get_motor_encoder(BP.PORT_A), \
                 BP.get_motor_encoder(BP.PORT_B), \
                 BP.get_motor_encoder(BP.PORT_C), \
                 BP.get_motor_encoder(BP.PORT_D)))

    def shutdown(self):
        BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
        BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
        BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
        BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))

        BP.reset_all()

    def set_speed(self, speed):
        self.desired_speed = speed
        self.moving = True
        self.pid.reset(self.desired_speed - self.current_speed)
        self.update()

    def straight(self):
        self.steer = 0

    def set_steer(self, direction, amount):
        if direction == 'right':
            self.steer = amount
        elif direction == 'left':
            self.steer = -amount
        if self.steer > 1:
            self.steer = 1
        elif self.steer < -1:
            self.steer = -1

    def turn_left(self):
        self.set_steer('left',1)

    def turn_right(self):
        self.set_steer('right', 1)

    def stop(self):
        self.moving = False
        self.set_motor(1, 0)
        self.set_motor(4, 0)



        self.set_motor(2, 0)
        self.set_motor(3, 0)

snot = mcms()

def test():
    while True:
        go = int(input('todo: '))
        if go == 1:
            snot.set_motor(1,-40)
            snot.set_motor(4,-40)
        elif go == 2:
            snot.set_motor(1,0)
            snot.set_motor(4,0)
        elif go == 3:
            snot.set_motor(1, 30)
            snot.set_motor(4, 10)
        elif go == 4:
            snot.set_motor(1, 10)
            snot.set_motor(4, 30)
        elif go == 5:
            snot.set_motor(3,20)
            time.sleep(0.3)
            snot.set_motor(3,0)
        elif go == 6:
            snot.set_motor(3,-20)
            time.sleep(0.3)
            snot.set_motor(3,0)
        elif go == 0:
            snot.stop()
            break

def yeet():
    while True:
        go = int(input('todo: '))
        if go == 1:
            snot.set_speed(2)
        elif go == 2:
            snot.set_speed(0)
        elif go == 3:
            snot.set_steer("right",0.2)
        elif go == 4:
            snot.set_steer("left", 0.2)
        elif go == 5:
            snot.straight()
        

def line_follow():
    snot.set_speed(-7)
    while not snot.get_touch():
        print(snot.get_nxt_light())
        snot.update()
        #snot.set_steer('right', (snot.get_nxt_light() - 2080)/400)



try:
    #todo: implement mcms push button controls
    #todo: implement line following control
    while True:
        go = int(input('what would you like to do: '))
        if go == 1:
            test()
        elif go == 2:
            yeet()
        elif go == 3:
            line_follow()
        elif go == 0:
            break

except KeyboardInterrupt:
    pass

snot.shutdown()
