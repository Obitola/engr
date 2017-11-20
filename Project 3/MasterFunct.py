import smbus
import time
bus = smbus.SMBus(1)
_slaveAddress = 0x6C
sensorPrecision = 10**5 #One less than in slave program?

def startPowerTracking(teamNumber):
    tNum = str(teamNumber)
    if (len(tNum) == 1):
        tNum = "0"+str(tNum)
    if (tNum.isdigit() == 0):
        print("ERROR: Invalid team number entered.")
        return -1
    data = [105, int(tNum[0]), int(tNum[1])]
    bus.write_i2c_block_data(_slaveAddress, 0, data)
    time.sleep(0.05)    
        
def getPowerProduced():
    try:
       x = bus.read_i2c_block_data(_slaveAddress, 112, 4)
    except:
        print("ERROR: Input/Output Error")
        x = [0, 0, 0, 0]

    ans = (x[0] << 24) | (x[1] << 16) | (x[2] << 8) | (x[3])
    time.sleep(0.05)
    
    if (255 == x[0] == x[1] == x[2] == x[3]):
        print("ERROR: Must start power tracking before requesting data.")
        return -1
    else:
        return float(ans) / sensorPrecision
    
    
def getPowerConsumed():
    try:
        x = bus.read_i2c_block_data(_slaveAddress, 99, 4)
    except:
        print("ERROR: Input/Output Error")
        x = [0, 0, 0, 0]
        
    ans = (x[0] << 24) | (x[1] << 16) | (x[2] << 8) | (x[3])
    time.sleep(0.1)
    if (255 == x[0] == x[1] == x[2] == x[3]):
        print("ERROR: Must start power tracking before requesting data.")
        return -1
    else:
        return float(ans) / sensorPrecision

def getPowerStored():
    try:
        x = bus.read_i2c_block_data(_slaveAddress, 98, 4)
    except:
        print("ERROR: Input/Output Error")
        x = [0, 0, 0, 0]

    ans = (x[0] << 24) | (x[1] << 16) | (x[2] << 8) | (x[3])
    time.sleep(0.1)
    if (255 == x[0] == x[1] == x[2] == x[3]):
        print("ERROR: Must start power tracking before requesting data.")
        return -1
    else:
        return float(ans) / sensorPrecision
