from __future__ import print_function  # use python 3 syntax but make it compatible with python 2
from __future__ import division  # ''

import time  # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers
import grovepi


BP = brickpi3.BrickPi3()  # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH)  # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.
ultrasonic_sensor_port = 4



class PID(object):
    """A generic PID loop controller which can be inherited and used in other control algorithms"""

    def __init__(self, startingError):
        """Return a instance of a un tuned PID controller"""
        self._p = 1
        self._i = 0
        self._d = 0
        self._esum = 0  # Error sum for integral term
        self._le = startingError  # Last error value

    def calculate(self, error, dt):
        """Calculates the output of the PID controller"""
        self._esum += error * dt
        dError = (error - self._le) / dt
        u = self._p * error + self._i * self._esum + self._d * dError
        self._le = error
        return u

    def reset(self, startingError):
        """Resets the integral sum and the last error value"""
        self._esum = 0
        self._le = startingError

def cm():
    return (snot.get_motor(1) + snot.get_motor(4)) / 2 * circumference / 360

class mcms(object):

    def __init__(self):
        self.previous_x = cm()
        self.previous_time = time.time() - 0.1
        self.previous_speed = 0
        self.delta_x = 0
        self.delta_time = 0.1
        self.delta_speed = 0
        self.current_x = 0
        self.current_time = time.time()
        self.current_speed = 0
        self.moving = False
        self.desired_speed = 0
        self.power = 0
        self.steer = 0
        self.pid = PID(0)
        self.power_= {'a': 0, 'b': 0, 'c': 0, 'd': 0}
        self.max_power = 400
        self.circumference = 27

    def update(self):
        self.current_x = cm()
        self.delta_x = self.current_x - self.previous

        self.current_time = time.time()
        self.delta_time = self.current_time - self.previous_time

        self.current_speed = self.delta_x/self.delta_time
        self.delta_speed = self.current_speed - self.previous_speed

        self.previous_x = self.current_time
        self.previous_time = self.current_time
        self.previous_speed = self.current_speed

        if self.moving:
            self.power += self.pid.calculate(self.desired_speed - self.current_speed, self.delta_time)#round((self.current_speed - self.desired_speed) / 2)
            self.set_motor(1,self.power * (1 + self.steer))
            self.set_motor(4,self.power * (1 - self.steer))

    # gets the distance value of the sensor
    def get_ultrasonic_distance(self):
        try:
            return grovepi.ultrasonicRead(ultrasonic_sensor_port)
        except brickpi3.SensorError:
            print('Error: Distance Sensor')

    # checks if button is pressed
    def get_touch(self):
        try:
            return BP.get_sensor(BP.PORT_2)
        except brickpi3.SensorError:
            print('Error: Touch Sensor')
            # sets the power for the given motor
    def get_wheel_distance(self):
        return (self.get_motor(1) + self.get_motor(4)) / 2 * self.circumference / 360

    def set_motor(self, motor, amount):
        if motor == 1 or motor == 'a':
            self.power['a'] = amount
        elif motor == 2 or motor == 'b':
            self.power['b'] = amount
        elif motor == 3 or motor == 'c':
            self.power['c'] = amount
        elif motor == 4 or motor == 'd':
            self.power['d'] = amount
        else:
            print('not a valid motor')

        if sum(self.power) > self.max_power:
            power_wheels = (self.max_power - self.power['b'] - self.power['c']) / (self.power['a'] + self.power['d'])
            BP.set_motor_power(BP.PORT_A, self.power['a'])
            BP.set_motor_power(BP.PORT_B, power_wheels * self.power['b'])
            BP.set_motor_power(BP.PORT_C, power_wheels * self.power['c'])
            BP.set_motor_power(BP.PORT_D, self.power['d'])

        else:
            BP.set_motor_power(BP.PORT_A, self.power['a'])
            BP.set_motor_power(BP.PORT_B, self.power['b'])
            BP.set_motor_power(BP.PORT_C, self.power['c'])
            BP.set_motor_power(BP.PORT_D, self.power['d'])
    # returns the orientation of the motor
    def get_motor(motor):
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

    def straight(self):
        self.steer = 0

    def set_steer(self, direction, amount):
        if direction == 'right':
            self.steer = amount
        elif direction == 'left':
            self.steer = -amount

    def turn_left(self):
        self.set_steer('left',1)

    def turn_right(self):
        self.set_steer('right', 1)

    def stop(self):
        self.moving = False
        self.set_motor(1, 0)
        self.set_motor(4, 0)

snot = mcms()



def userControl():
    go = input('How to move:')
    while True:
        go = input('How to move:')
        if go == 'r':
            snot.set_steer('left', 0.3)
        elif go == 'l':
            snot.set_steer('right', 0.3)
            snot.steer('right',)
        elif go == 'm':
            snot.set_speed(20)
        elif go == 's':
            snot.stop()
        elif go == 'b':
            snot.set_speed(-15)
        elif go == 'stop':
            break

try:
    while True:
        do = input('What would you like to do')
        if do == 'shutdown':
            snot.shutdown()
            break
        elif do == 'ctrl':
            userControl()



except KeyboardInterrupt:
    pass

snot.shutdown()
