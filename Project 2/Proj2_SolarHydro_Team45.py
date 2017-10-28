from math import pow, pi, ceil

#converts between Joules and MWH
def mwhToJoules(energy):
    return energy * 3600000000

#converts between Joules and MWH
def joulesToMwh(energy):
    return energy / 3600000000

#functions needed
def energyIn():
    return (energy_out + turbineLoss() + pipeFrictionUp() + pipeFrictionDown() + fittingLoss())/pump_efficiency


def systemEfficiency():
    return energy_out / energyIn()

def fillTime():
    if flow_rate_pump <= flow_rate_turbine:
        return 12
    else:
        return 12 * flow_rate_turbine / flow_rate_pump

def emptyTime():
    if flow_rate_turbine <= flow_rate_pump:
        return 12
    else:
        return 12 * flow_rate_pump / flow_rate_turbine

def velocityUp():
    return flow_rate_pump / pipeArea()


def velocityDown():
    return flow_rate_turbine / pipeArea()

def effectiveElevation():
    return reservoirDepth() / 2 + bottomReservoirElevation()

def pipeArea():
    return pi * pow(pipe_diameter, 2) / 4

def pumpLoss():
    return (1 - pump_efficiency) * energyIn()

def turbineLoss():
    return energy_out * (1 / turbine_efficiency - 1)

def pipeFrictionUp():
    return waterMass() * (pipe_friction_factor * pipeLength() * pow(velocityUp(), 2) / (2 * pipe_diameter))

def pipeFrictionDown():
    return waterMass() * (pipe_friction_factor * pipeLength() * pow(velocityDown(), 2) / (2 * pipe_diameter))

def fittingLoss():
    sum = 0
    sum += waterMass() * bendCoefficient1() * (pow(velocityUp(), 2) + pow(velocityDown(),2))
    sum += waterMass() * bendCoefficient2() * (pow(velocityUp(), 2) + pow(velocityDown(), 2))
    sum += waterMass() * bendCoefficient3() * (pow(velocityUp(), 2) + pow(velocityDown(), 2))
    sum += waterMass() * bendCoefficient4() * (pow(velocityUp(), 2) + pow(velocityDown(), 2))
    return sum / 2

def volume():
    return waterMass() / water_density

def waterMass():
    if flow_rate_pump>= flow_rate_turbine:
        return 12 * 60 * 60 * flow_rate_pump * water_density
    else:
        return 12 * 60 * 60 * flow_rate_turbine * water_density

zone = 1

def costZone():
	if zone == 1
  		sitePrepCost = (.25 * surfaceArea()) + 40000 + 8000
      	bendCoefficient1 = .15
        bendCoefficient2 = .15
		bendCoefficient3 = 0
    elif zone == 2
    	sitePrepCost  = (.5 * surfaceArea()) + 100000 + 2000
      	bendCoefficient1 = .22
		bendCoefficient2 = .22
		bendCoefficient3 = 0
    elif zone == 3
    	sitePrepCost = (.3*surfaceArea())+(.6*surfaceArea()) +150000
     	bendCoefficient1 = .1
		bendCoefficient2 = .15
		bendCoefficient3 = .22
    else 
    	print("Error: Zone input invalid")
pumpHouseCost = 100000
wallHeight = reservoirDepth()
perimeter = 2*pi*sqrt(surfaceArea()/pi)
def wallHeightCost():
	if wallHeight < 7.5 and wallHeight >= 5 
  		wallHeightCost = 30 + (wallHeight - 5)*(60-30)/(2.5)
  	elif wallHeight < 10 and wallHeight >= 7.5
    	wallHeightCost  60 + (wallHeight-7.5)*(95-60)/2.5
    elif wallHeight < 12.5 and wallHeight >= 10
    	wallHeightCost = 95 +(wallHeight - 10)*(135-95)/2.5
    elif wallHeight < 15 and wallHeight >= 12.5
    	wallHeightCost = 135 + (wallHeight - 12.5)*(180-135)/2.5
    elif wallHeight < 17.5 and wallHeight >= 15
    	wallHeightCost = 180 + (wallHeight - 15)*(250-180)/2.5
    elif wallHeight < 20 and wallHeight >= 17.5
    	wallHeightCost = 250 + (wallHeight - 17.5)*(340-250)/2.5
    elif wallHeight == 20
    	wallHeightCost = 340
    else
    	print('Wall Height must be [5,20] meters')
    return wallHeightCost

  
def pumpCost():
    return flow_rate_pump * pumpFoundry()

def pipeCost():
    return pipeShack() * pipe_length

def turbineCost():
    return turbinesW() * flow_rate_turbine

def pumpHouseCost():
    return pumphouseCost

def bendCost()
	return bendFittings1()+bendFittings2()+bendFittings3()

def sitePrepCost():
    return sitePrepCost

def perimeterWallCost():
    return perimeter * wallHeightCost()

def pipeInstallCost():
    return 500 * pipe_length

def raisedPipeCost():
    if zone == 1
    	raisedPipe = 0
      	raisedPipeArea = 0
    elif zone == 2
    	raisedPipe = 0
     	 raisedPipeArea = 0
    else 
    	raisedPipeLength = 0
      	raisedPipeArea = 0
    return 50 *raisedPipeLength + 250 * raisedPipeArea
    
def otherCosts():
    return 0

def cost():
    sum = 0
    sum += pumpCost()
    sum += pipeCost()
    sum += turbineCost()
    sum += pumpHouseCost()
    sum += sitePrepCost()
    sum += perimeterWallCost()
    sum += pipeInstallCost()
    sum += raisedPipeCost()
    sum += otherCosts()
    return sum

#returns $ per m3 / sec of flow
def pumpFoundry():
    x = ceil(int(( effectiveElevation() / 10 ) - 2))
    if pump_efficiency == 'cheap' or pump_efficiency == 0.80:
        y = 0
    elif pump_efficiency == 'value' or pump_efficiency == 0.83:
        y = 1
    elif pump_efficiency == 'standard' or pump_efficiency == 0.86:
        y = 2
    elif pump_efficiency == 'high-grade' or pump_efficiency == 0.89:
        y = 3
    elif pump_efficiency == 'premium' or pump_efficiency == 0.92:
        y = 4
    efficiency = [[200,240,288,346,415]]
    efficiency.append([220,264,317,380,456])
    efficiency.append([242,290,348,418,502])
    efficiency.append([266,319,383,460,552])
    efficiency.append([293,351,422,506,607])
    efficiency.append([322,387,464,557,668])
    efficiency.append([354,425,510,612,735])
    efficiency.append([390,468,561,673,808])
    efficiency.append([429,514,617,741,889])
    efficiency.append([472,566,679,815,978])
    efficiency.append([519,622,747,896,1076])
    return efficiency[x][y]

#returns $ / m
def pipeShack():
    x = int(round(pipe_diameter * 4))
    if pipe_friction_factor == 'salvage' or pipe_friction_factor == 0.05:
        y = 0
    elif pipe_friction_factor == 'questionable' or pipe_friction_factor == 0.03:
        y = 1
    elif pipe_friction_factor == 'better' or pipe_friction_factor == 0.02:
        y = 2
    elif pipe_friction_factor == 'nice' or pipe_friction_factor == 0.01:
        y = 3
    elif pipe_friction_factor == 'premium' or pipe_friction_factor == 0.005:
        y = 4
    elif pipe_friction_factor == 'glorious' or pipe_friction_factor == 0.002:
        y = 5
    efficiency = [[1.00,1.20,1.44,2.16,2.70,2.97]]
    efficiency.append([1.20,1.44,1.72,2.58,3.23,3.55])
    efficiency.append([2.57,3.08,3.70,5.55,6.94,7.64])
    efficiency.append([6.30,7.56,9.07,14,17,19])
    efficiency.append([14,16,20,29,37,40])
    efficiency.append([26,31,37,55,69,76])
    efficiency.append([43,52,63,94,117,129])
    efficiency.append([68,82,98,148,185,203])
    efficiency.append([102,122,146,219,274,302])
    efficiency.append([144,173,208,311,389,428])
    efficiency.append([197,237,284,426,533,586])
    efficiency.append([262,315,378,567,708,779])
    efficiency.append([340,408,490,735,919,1011])
    return(efficiency[x][y])

#returns $ / bend
def bendFittings1():
    x = int(round(pipe_diameter * 4))
    if bendCoefficient1() == 20 or bendCoefficient1() == 0.1:
        y = 0
    elif bendCoefficient1() == 30 or bendCoefficient1() == 0.15:
        y = 1
    elif bendCoefficient1() == 45 or bendCoefficient1() == 0.2:
        y = 2
    elif bendCoefficient1() == 60 or bendCoefficient1() == 0.22:
        y = 3
    elif bendCoefficient1() == 75 or bendCoefficient1() == 0.27:
        y = 4
    elif bendCoefficient1() == 90 or bendCoefficient1() == 0.3:
        y = 5
    efficiency = [[1.00,1.05,1.10,1.16,1.22,1.28,0.10]]
    efficiency.append([1.49,1.57,1.64,1.73,1.81,1.90,0.25])
    efficiency.append([4.93,5.17,5.43,5.70,5.99,7,0.50])
    efficiency.append([14,15,16,16,17,18,0.75])
    efficiency.append([32,34,36,38,39,41,1.00])
    efficiency.append([62,65,69,72,76,80,1.25])
    efficiency.append([107,112,118,124,130,137,1.50])
    efficiency.append([169,178,187,196,206,216,1.75])
    efficiency.append([252,265,278,292,307,322,2.00])
    efficiency.append([359,377,396,415,436,458,2.25])
    efficiency.append([492,516,542,569,598,628,2.50])
    efficiency.append([654,687,721,757,795,835,2.75])
    efficiency.append([849,892,936,983,1032,1084,3.00])
    return(efficiency[x][y])

#returns $ / bend
def bendFittings2():
    x = int(round(pipe_diameter * 4))
    if bendCoefficient2() == 20 or bendCoefficient2() == 0.1:
        y = 0
    elif bendCoefficient2() == 30 or bendCoefficient2() == 0.15:
        y = 1
    elif bendCoefficient2() == 45 or bendCoefficient2() == 0.2:
        y = 2
    elif bendCoefficient2() == 60 or bendCoefficient2() == 0.22:
        y = 3
    elif bendCoefficient2() == 75 or bendCoefficient2() == 0.27:
        y = 4
    elif bendCoefficient2() == 90 or bendCoefficient2() == 0.3:
        y = 5
    efficiency = [[1.00,1.05,1.10,1.16,1.22,1.28,0.10]]
    efficiency.append([1.49,1.57,1.64,1.73,1.81,1.90,0.25])
    efficiency.append([4.93,5.17,5.43,5.70,5.99,7,0.50])
    efficiency.append([14,15,16,16,17,18,0.75])
    efficiency.append([32,34,36,38,39,41,1.00])
    efficiency.append([62,65,69,72,76,80,1.25])
    efficiency.append([107,112,118,124,130,137,1.50])
    efficiency.append([169,178,187,196,206,216,1.75])
    efficiency.append([252,265,278,292,307,322,2.00])
    efficiency.append([359,377,396,415,436,458,2.25])
    efficiency.append([492,516,542,569,598,628,2.50])
    efficiency.append([654,687,721,757,795,835,2.75])
    efficiency.append([849,892,936,983,1032,1084,3.00])
    return(efficiency[x][y])

#returns $ / bend
def bendFittings3():
    x = int(round(pipe_diameter * 4))
    if bendCoefficient3() == 20 or bendCoefficient3() == 0.1:
        y = 0
    elif bendCoefficient3() == 30 or bendCoefficient3() == 0.15:
        y = 1
    elif bendCoefficient3() == 45 or bendCoefficient3() == 0.2:
        y = 2
    elif bendCoefficient3() == 60 or bendCoefficient3() == 0.22:
        y = 3
    elif bendCoefficient3() == 75 or bendCoefficient3() == 0.27:
        y = 4
    elif bendCoefficient3() == 90 or bendCoefficient3() == 0.3:
        y = 5
    efficiency = [[1.00,1.05,1.10,1.16,1.22,1.28,0.10]]
    efficiency.append([1.49,1.57,1.64,1.73,1.81,1.90,0.25])
    efficiency.append([4.93,5.17,5.43,5.70,5.99,7,0.50])
    efficiency.append([14,15,16,16,17,18,0.75])
    efficiency.append([32,34,36,38,39,41,1.00])
    efficiency.append([62,65,69,72,76,80,1.25])
    efficiency.append([107,112,118,124,130,137,1.50])
    efficiency.append([169,178,187,196,206,216,1.75])
    efficiency.append([252,265,278,292,307,322,2.00])
    efficiency.append([359,377,396,415,436,458,2.25])
    efficiency.append([492,516,542,569,598,628,2.50])
    efficiency.append([654,687,721,757,795,835,2.75])
    efficiency.append([849,892,936,983,1032,1084,3.00])
    return(efficiency[x][y])

#returns $ / bend
def bendFittings4():
    x = int(round(pipe_diameter * 4))
    if bendCoefficient4() == 20 or bendCoefficient4() == 0.1:
        y = 0
    elif bendCoefficient4() == 30 or bendCoefficient4() == 0.15:
        y = 1
    elif bendCoefficient4() == 45 or bendCoefficient4() == 0.2:
        y = 2
    elif bendCoefficient4() == 60 or bendCoefficient4() == 0.22:
        y = 3
    elif bendCoefficient4() == 75 or bendCoefficient4() == 0.27:
        y = 4
    elif bendCoefficient4() == 90 or bendCoefficient4() == 0.3:
        y = 5
    efficiency = [[1.00,1.05,1.10,1.16,1.22,1.28,0.10]]
    efficiency.append([1.49,1.57,1.64,1.73,1.81,1.90,0.25])
    efficiency.append([4.93,5.17,5.43,5.70,5.99,7,0.50])
    efficiency.append([14,15,16,16,17,18,0.75])
    efficiency.append([32,34,36,38,39,41,1.00])
    efficiency.append([62,65,69,72,76,80,1.25])
    efficiency.append([107,112,118,124,130,137,1.50])
    efficiency.append([169,178,187,196,206,216,1.75])
    efficiency.append([252,265,278,292,307,322,2.00])
    efficiency.append([359,377,396,415,436,458,2.25])
    efficiency.append([492,516,542,569,598,628,2.50])
    efficiency.append([654,687,721,757,795,835,2.75])
    efficiency.append([849,892,936,983,1032,1084,3.00])
    return(efficiency[x][y])

#returns $ per m^3 / sec of flow
def turbinesW():
    x = ceil(int((effectiveElevation() / 10) - 2))
    if turbine_efficiency == 'meh' or turbine_efficiency == 0.83:
        y = 0
    elif turbine_efficiency == 'good' or turbine_efficiency == 0.86:
        y = 1
    elif turbine_efficiency == 'fine' or turbine_efficiency == 0.89:
        y = 2
    elif turbine_efficiency == 'super' or turbine_efficiency == 0.92:
        y = 3
    elif turbine_efficiency == 'mondo' or turbine_efficiency == 0.94:
        y = 4
    efficiency = [[360, 432, 518, 622, 746]]
    efficiency.append([396, 475, 570, 684, 821])
    efficiency.append([436, 523, 627, 753, 903])
    efficiency.append([479, 575, 690, 828, 994])
    efficiency.append([527, 632, 759, 911, 1093])
    efficiency.append([580, 696, 835, 1002, 1202])
    efficiency.append([638, 765, 918, 1102, 1322])
    efficiency.append([702, 842, 1010, 1212, 1455])
    efficiency.append([772, 926, 1111, 1333, 1600])
    efficiency.append([849, 1019, 1222, 1467, 1760])
    efficiency.append([934, 1120, 1345, 1614, 1936])
    return (efficiency[x][y])

#pumps = ['cheap','value','standard','high-grade','premium']
pumps = [0.8,0.83,0.86,0.89,0.92]
#pipes = ['salvage','questionable','better','nice','premium','glorious']
pipes = [0.05,0.03,0.02,0.01,0.005,0.002]
bends = [0.1,0.15,0.2,0.22,0.27,0.3]
#turbines = ['meh','good','fine','super','mondo']
turbines = [0.83,0.86,0.89,0.92,0.94]

effective_performance_ratings = [x for x in range(20, 130, 10)]
internal_diameters = [x/4.0 for x in range(0,13)]
internal_diameters[0] = 0.1

#given
energy_out = mwhToJoules(120)
gravity = 9.81
water_density = 1000

#shop inputs
pump_efficiency = 0.9
turbine_efficiency = 0.92
pipe_friction_factor = 0.05

#model inputs
zones = [1,2,3]
def bottomReservoirElevation():
    if zone == 1:
        return 50

def pipeLength():
    if zone == 1:
        return 75



#we choose
#range()
flow_rate_pump = 65
#range()
flow_rate_turbine = 30

#one or the other
#range()
#reservoir_depth = 10
#range(<600**2)
reservoir_surface_area = pow(600,2)

# #outputs
# reservoir_surface_area  surfaceArea()
# energy_in               energyIn()
# system_efficiency       systemEfficiency()
# fill_time               fillTime()
# empty_time              emptyTime()

for pump_efficiency in pumps:
    for pipe_friction_factor in pipes:
        for turbine_efficiency in turbines:
                for pipe_diameter in internal_diameters:
                    for zone in zones:
                        if effectiveElevation() <= 120:
                            print('Energy In:',joulesToMwh(energyIn()))
                            print('Efficiency:',systemEfficiency())
                        else:
                            print("error:", effectiveElevation())
