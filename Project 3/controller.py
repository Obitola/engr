from __future__ import print_function  # use python 3 syntax but make it compatible with python 2
from __future__ import division  # ''

import time  # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers
import grovepi
import pygame



BP = brickpi3.BrickPi3()  # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH) # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.

ultrasonic_sensor_port = 4

#A generic PID loop controller for control algorithms
class PID(object):

    # Return a instance of a un tuned PID controller
    def __init__(self, startingError):
        self._p = 0.1
        self._i = 0
        self._d = 0.1
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
        self.previous_x = 0
        self.previous_time = time.time() - 0.1
        self.previous_speed = 0
        self.current_speed = 0
        self.moving = False
        self.desired_speed = 0
        self.power = 0
        self.steer = 0
        self.pid = PID(0)
        self.power_= [0,0,0,0,0]
        self.max_power = 100
        self.circumference = 27
        self.desired_speed = 0

    def update(self):
        self.current_speed = (self.get_wheel_distance() - self.previous_x) / (time.time() - self.previous_time)

        if self.moving:
            self.desired_x = self.desired_speed (time.time() - self.previous_time) + self.previous_x
            self.power += self.pid.calculate((self.desired_x - self.get_wheel_distance()), time.time() - self.previous_time())#round((self.current_speed - self.desired_speed) / 2)
            self.set_motor(1,self.power * (1 + self.steer))
            self.set_motor(4,self.power * (1 - self.steer))

        self.previous_x = self.get_wheel_distance()
        self.previous_time = time.time()
        self.previous_speed = self.current_speed
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

    def get_wheel_distance(self):
        return ((self.get_motor(1) + self.get_motor(4)) / 2) * (27 / 360)

    def set_motor(self, motor, amount):
        self.power[motor] = amount

        if sum(self.power) > self.max_power:
            power_wheels = (self.max_power - self.power[2] - self.power[3]) / (self.power[1] + self.power[4])
            BP.set_motor_power(BP.PORT_A, power_wheels * self.power[1])
            BP.set_motor_power(BP.PORT_B, self.power[2])
            BP.set_motor_power(BP.PORT_C, self.power[3])
            BP.set_motor_power(BP.PORT_D, power_wheels * self.power[4])

        else:
            BP.set_motor_power(BP.PORT_A, self.power[1])
            BP.set_motor_power(BP.PORT_B, self.power[2])
            BP.set_motor_power(BP.PORT_C, self.power[3])
            BP.set_motor_power(BP.PORT_D, self.power[4])

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
        self.pid.reset(0)
        self.desired_x = self.current_x
        self.update()

    def straight(self):
        self.steer = 0

    def set_steer(self, direction, amount):
        if direction == 'right':
            self.steer += amount
        elif direction == 'left':
            self.steer -= -amount
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
        go = input('todo')
        if go == 'f':
            snot.set_motor(1,20)
            snot.set_motor(4,20)
        elif go == 's':
            snot.set_motor(1,0)
            snot.set_motor(4,0)
        elif go == 'r':
            snot.set_motor(1, 30)
            snot.set_motor(4, 10)
        elif go == 'l':
            snot.set_motor(1, 10)
            snot.set_motor(4, 30)
        elif go == 'stop':
            snot.stop()
            break

try:
    #todo: implement mcms push button controls
    #todo: implement line following control
    while True:
        go = input('what would you like to do')
        if go == 'test':
            test()
        elif go == 'stop':
            break

except KeyboardInterrupt:
    pass

snot.shutdown()