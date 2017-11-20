import time
import brickpi3
from MPU9250 import MPU9250

BP = brickpi3.BrickPi3()

m = MPU9250()

try:
    while True:
        gyro = m.readGyro()
        print(gyro['z'])
except KeyboardInterrupt:
    pass