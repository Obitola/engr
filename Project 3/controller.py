from __future__ import print_function  # use python 3 syntax but make it compatible with python 2
from __future__ import division  # ''

import time  # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers
#import grovepi
import MasterFunct as pmad
import smbus
from math import pi


BP = brickpi3.BrickPi3()  # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH) # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_LIGHT_ON)
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.NXT_LIGHT_ON)

ultrasonic_sensor_port = 4
white = 2100
black = 2700

#A generic PID loop controller for control algorithms
class PID(object):

    # Return a instance of a un tuned PID controller
    def __init__(self, startingError):
        self._p = 0.5
        self._i = 0.03
        self._d = 0.2
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
        self.previous_x_right = self.get_wheel_distance_right()
        self.previous_x_left = self.get_wheel_distance_left()
        self.previous_time = time.time() - 0.1
        self.current_speed = 0.0
        self.current_speed_right = 0.0
        self.current_speed_left = 0.0
        self.moving = False
        self.desired_speed = 0.0
        self.desired_speed_right = 0.0
        self.desired_speed_left = 0.0
        self.power_right = 0
        self.power_left = 0
        self.steer = 0
        self.pid_right = PID(0)
        self.pid_left = PID(0)
        self.power_list = [0,0,0,0,0]
        self.max_power = 70
        self.radius = 27
        self.desired_speed = 0.0

    def update(self):
        delta_time = time.time() - self.previous_time

        self.desired_speed_right = self.desired_speed * (1 + self.steer)
        self.desired_speed_left = self.desired_speed * (1 - self.steer)

        self.current_speed_right = (self.get_wheel_distance_right() - self.previous_x_right) / (delta_time)
        self.current_speed_left = (self.get_wheel_distance_left() - self.previous_x_left) / (delta_time)
        self.current_speed = (self.current_speed_right + self.current_speed_left) / 2

        error_right = self.desired_speed_right - self.current_speed_right
        error_left = self.desired_speed_left - self.current_speed_left

        #if self.moving:
        self.power_right += self.pid_right.calculate(error_right, delta_time)
        self.power_left += self.pid_left.calculate(error_left, delta_time)

        self.set_motor(1,self.power_right)
        self.set_motor(4,self.power_left)

        self.previous_x_right = self.get_wheel_distance_right()
        self.previous_x_left = self.get_wheel_distance_left()
        self.previous_time = time.time()

        self.data()
        time.sleep(0.2)

    def move_distance(self, distance, speed):
        self.set_speed(speed)
        self.steer = 0
        start_time = time.time()
        total_time = abs(distance / speed)
        while time.time() - start_time < total_time:
            self.update()
        self.stop()

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

    def get_wheel_distance_right(self):
        return self.get_motor(1) * (2 * pi * 3.5 / 360)

    def get_wheel_distance_left(self):
        return self.get_motor(4) * (2 * pi * 3.5 / 360)

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
        print("Speed: %6d Light: %6d  Hall: %6d" \
              % (self.current_speed, \
                 self.get_nxt_light(), \
                 self.get_hall_sensor()))

    def shutdown(self):
        BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
        BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
        BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
        BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))

        BP.reset_all()

    def set_speed(self, speed):
        self.desired_speed = speed
        self.desired_speed_right = self.desired_speed * (1 + self.steer)
        self.desired_speed_left = self.desired_speed * (1 - self.steer)
        self.moving = True
        self.update()

    def straight(self):
        self.steer = 0

    def set_steer(self, direction, amount):
        if direction == 'right':
            self.steer = amount
        elif direction == 'left':
            self.steer = -amount
        if self.steer > 1.5:
            self.steer = 1.5
        elif self.steer < -1.5:
            self.steer = -1.5

    def turn_left(self):
        self.set_steer('left',1)

    def turn_right(self):
        self.set_steer('right', 1)

    def stop(self):
        self.desired_speed = 0
        self.set_motor(1, 0)
        self.set_motor(4, 0)
        self.set_motor(2, 0)
        self.set_motor(3, 0)

    def open_claw(self):
        for x in range(16):
            snot.set_motor(3, 20)
            time.sleep(0.3)
            snot.set_motor(3, 0)
            time.sleep(0.1)

    def close_claw(self):
        for x in range(16):
            snot.set_motor(3, -20)
            time.sleep(0.3)
            snot.set_motor(3, 0)
            time.sleep(0.1)

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
    snot.set_speed(-4)
    snot.update()
    while not snot.get_touch():
        snot.data()
        snot.set_steer('right', (snot.get_nxt_light() - ((white + black) / 2))/400)
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

try:
    #todo: implement mcms push button controls
    #todo: implement line following control
    go = 9
    while True:
        try:
            go = int(input('what would you like to do: '))
        except:
            print('Please input an integer')
        if go == 1:
            test()
        elif go == 2:
            yeet()
        elif go == 3:
            line_follow()
        elif go == 4:
            energy()
        elif go == 5:
            data()
        elif go == 0:
            break

except KeyboardInterrupt:
    pass

snot.shutdown()
