# Project 3
# File: Proj2_SolarHydro_Team45.py
# Date: 8 December 2017
# By: Oluwatobi Ola
# olao
# Evelyn Nonamaker
# enonamak
# Haydn Schroader
# hschroad
# Paul Thomas
# thoma695
# Section: 3
# Team: 45
#
# ELECTRONIC SIGNATURE
# Oluwatobi Ola
# Evelyn Nonamaker
# Haydn Schroader
# Paul Thomas
#
# The electronic signatures above indicate that the program
# submitted for evaluation is the combined effort of all
# team members and that each member of the team was an
# equal participant in its creation. In addition, each
# member of the team has a general understanding of
# all aspects of the program development and execution.
#
# It makes our robot move, follow lines, drop cargo and find magnets

from __future__ import print_function  # use python 3 syntax but make it compatible with python 2
from __future__ import division  # ''

import time  # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers
#import grovepi
import MasterFunct as pmad
import smbus
from math import pi

BP = brickpi3.BrickPi3()  # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)  # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_LIGHT_ON)
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.TOUCH)
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.NXT_LIGHT_ON)

ultrasonic_sensor_port = 4
white = 2460
black = 2710
radius = 4
speed = -5
hall_normal = 2065
hall_error = 30
black_resistance = 0.3
sensitivity = 3.5
buffer = 0.005
min_energy = 120
try:
    pmad.startPowerTracking(45)
except:
    print('PMAD not connected')
# Same pid currently being implemented in Purdue's IEEE ROV team
# A generic PID loop controller for control algorithms
class PID(object):
    # Return a instance of a un tuned PID controller
    def __init__(self):
        self._p = 1.0
        self._i = 0
        self._d = 0
        self._esum = 0  # Error sum for integral term
        #self._le = startingError  # Last error value

    # Calculates the output of the PID controller
    def calculate(self, error):
        #self._esum += error * dt
        #dError = (error - self._le) / dt
        u = self._p * error # + self._i * self._esum + self._d * dError
        #self._le = error
        return u

    # Resets the integral sum and the last error value
    def reset(self):
        pass
        #self._esum = 0
        #self._le = startingError

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
    def get_touch(self, sensor):
        try:
            if sensor == 1:
                return BP.get_sensor(BP.PORT_1)
            elif sensor == 3:
                return BP.get_sensor(BP.PORT_3)
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
        print("Speed: %3f Light: %6d  Hall: %6d  Steer: %3f " \
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
        self.speed = speed #* ((4 - abs(self.steer)) / 4) 
        dps = speed * 360 / (2 * pi * radius)
        dps_right = dps * (1 + self.steer)
        dps_left = dps * (1 - self.steer)
        self.set_dps(4, dps_right)
        self.set_dps(1, dps_left)

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
        self.set_speed(0)
        self.update()
        self.set_motor(1, 0)
        self.set_motor(4, 0)
        self.set_motor(2, 0)
        self.set_motor(3, 0)

    def open_claw(self):
        start = pmad.getPowerStored()
        for x in range(30):
            snot.set_motor(3, 13)
            time.sleep(0.2)
            snot.set_motor(3, 0)
            time.sleep(0.1)
        print('Energy Used to Open Claw', start - pmad.getPowerStored())

    def close_claw(self):
        start = pmad.getPowerStored()
        for x in range(22):
            snot.set_motor(3, -20)
            time.sleep(0.3)
            snot.set_motor(3, 0)
            time.sleep(0.1)
        print('Energy Used to Close Claw', start - pmad.getPowerStored())

snot = mcms()

def wait_for_touch():
    count = 0
    while not snot.get_touch(1):
        if snot.get_touch(3):
            print('hehe')
            count += 1
            move(0,1)
            time.sleep(1)
    return count

def wait_for_energy():
    try:
        while pmad.getPowerStored() < min_energy:
            time.sleep(0.1)
    except:
        print('Error')

def calculate_steer():
    sum = black + white
    difference = black - white
    value = ((snot.get_nxt_light() - (sum - (difference * black_resistance))/2)  / ((difference) /  sensitivity))
    snot.set_steer('left',value)
    snot.update()

def line_follow(distance):
    length = abs(distance / speed)
    start_time = time.time()
    snot.set_speed(speed)
    snot.update()
    while time.time() - start_time < length:
        calculate_steer()
        time.sleep(buffer)
    snot.stop()

def navigate_to_hall():
    snot.set_speed(speed)
    snot.update()
    while check_hall():
        calculate_steer()
        time.sleep(buffer)
    snot.stop()

def move(steer, distance):
    length = abs(distance / speed)
    start_time = time.time()
    snot.set_speed(speed)
    snot.set_steer('right', steer)
    snot.update()
    while time.time() - start_time < length:
        time.sleep(buffer)
    snot.stop()

def energy():
    pmad.startPowerTracking(45)
    start_energy = pmad.getPowerStored()
    length = 10
    start_time = time.time()
    snot.set_speed(0)
    snot.update()
    while time.time() - start_time < length:
        time.sleep(buffer)
    snot.stop()
    print("Energy Used: ", start_energy - pmad.getPowerStored())
    
    
    start_energy = pmad.getPowerStored()
    total_power = 0
    snot.set_speed(0)
    while pmad.getPowerStored() >= 50:
        snot.update()
        #print("Produced: ", pmad.getPowerProduced(),"\tConsumed: ", pmad.getPowerConsumed(),"\tStored: ", pmad.getPowerStored())
    snot.stop()
    print(start_energy - pmad.getPowerStored())

def data():
    while True:
        snot.data()
        time.sleep(0.5)

def drop_off():
    snot.open_claw()

def legit():
    #pmad.startPowerTracking(45)
    location = 'null'
    while location == 'null':
        print('select location')
        input = wait_for_touch()
        if input == 1:
            location = 'A'
        elif input == 2:
            location = 'B'
        elif input == 3:
            location = 'C'

    print('waiting till cargo is held')
    wait_for_touch()
    snot.close_claw()

    wait_for_touch()

    print('traveling with cargo')
    navigate_to_hall()

    print('reached beacon A')
    if location == 'A':
        move(0.2, 15)
        navigate_to_hall()
        print('reached drop-off site A')
    elif location == 'B':
        line_follow(20)
        navigate_to_hall()
        print('reached beacon B')
        move(0.4, 7)
        line_follow(15)
        navigate_to_hall()
        print('reached drop-off site B')

    elif location == 'C':
        line_follow(20)
        navigate_to_hall()
        print('reached beacon B')
        line_follow(20)
        navigate_to_hall()
        print('reached beacon C')
        move(0.4, 7)
        line_follow(15)
        navigate_to_hall()
        print('reached drop-off site C')

    print('reached drop-off location')
    move(-0.31, 28)
    drop_off()
    move(0.2, 4)

    print('navigate back to line')
    print('returning to pickup location')
    navigate_to_hall()

def check_hall():
    average = 0
    for x in range(10):
        average += snot.get_hall_sensor()
    average = average / 10
    return average < hall_normal + hall_error and average > hall_normal - hall_error

try:
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
        elif go == 3:
            snot.open_claw()
        elif go == 4:
            move(0,30)
        elif go == 5:
            data()
        elif go == 6:
            energy()
        elif go == 7:
            line_follow(80)
        elif go == 0:
            break

except KeyboardInterrupt:
    pass

snot.shutdown()
