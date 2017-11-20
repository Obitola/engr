import smbus
import time

import MasterFunct

MasterFunct.startPowerTracking(2)

while(1):
    print("Produced: ", MasterFunct.getPowerProduced(),"\tConsumed: ", MasterFunct.getPowerConsumed(),"\tStored: ", MasterFunct.getPowerStored())
    
