from math import pow, pi

#given
energy_out = 120
gravity = 9.81
water_density = 1000

# #inputs
# pump_efficiency
# turbine_efficiency
# pipe_diameter
pipe_length = 50
# pipe_friction_factor
reservoir_depth = 10
bottom_reservoir_elevation = 20
# flow_rate_pump =
# flow_rate_turbine =
# bend_coefficient_1 = input("Enter bent coefficient #1:")
# bend_coefficient_2 = input("Enter bend coefficient #2:")

#intermediate variables

# #outputs
# reservoir_surface_area
# energy_in
# system_efficiency
# fill_time
# empty_time

#functions needed

def fill_time():
    return volume / volumetric_flow_rate_up

def empty_time():
    return volume / volumetric_flow_rate_down

def velocityUp():
    pass

def velocityDown():
    pass

def effectiveElevation(height, depth):
    return height + bottom_reservoir_elevation

def mwhToJoules(energy):
    return energy * 3600000

def joulesToMwh(energy):
    return energy / 3600000

def energyIn():
    pass

def pipeArea(diameter):
    return pi * pow(diameter, 2) / 4

def energyPumpLoss(pipe_efficiency,energy_in):
    return (1 - pipe_efficiency) * energy_in

def energyTurbineLoss(turbine_efficiency):
    return energy_out * (1 / turbine_efficiency - 1)

def energyPipeFrictionUp(water_mass, pipe_friction_factor, velocity_up, pipe_diameter):
    return water_mass * (pipe_friction_factor * pipe_length * pow(velocity_up, 2) / (2 * pipe_diameter))

def energyPipeFrictionDown(water_mass, pipe_friction_factor, velocity_down, pipe_diameter):
    return water_mass * (pipe_friction_factor * pipe_length * pow(velocity_down, 2) / (2 * pipe_diameter))

def energyFittingLoss(water_mass, fitting_constant, velocity_down):
    return water_mass * fitting_constant * pow(velocity_down, 2) / 2

def energyOut(pump,turbine,pipe_up,pipe_down,fitting,energy_in):
    return energy_in - pump - turbine - pipe_up - pipe_down - fitting

def massWater(water_density, volumetric_flow_rate, fill_time):
    return water_density * volumetric_flow_rate * fill_time

def fill_time(volume, volumetric_flow_rate):
    return volume / volumetric_flow_rate

def volumetricFlowRate(pipe_area, velocity):
    return pipe_area * velocity

#returns $ per m3 / sec of flow
def pumpFoundry(product_line, meters):
    x = int(( meters / 10 ) - 2)
    if product_line == 'cheap' or product_line == 0.80:
        y = 0
    elif product_line == 'value' or product_line == 0.83:
        y = 1
    elif product_line == 'standard' or product_line == 0.86:
        y = 2
    elif product_line == 'high-grade' or product_line == 0.89:
        y = 3
    elif product_line == 'premium' or product_line == 0.92:
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
def pipeShack(product_line, diameter):
    x = int(round(diameter * 4))
    if product_line == 'salvage' or product_line == 0.05:
        y = 0
    elif product_line == 'questionable' or product_line == 0.03:
        y = 1
    elif product_line == 'better' or product_line == 0.02:
        y = 2
    elif product_line == 'nice' or product_line == 0.01:
        y = 3
    elif product_line == 'premium' or product_line == 0.005:
        y = 4
    elif product_line == 'glorious' or product_line == 0.002:
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
def bendFittings(angle, diameter):
    x = int(round(diameter * 4))
    if angle == 20 or angle == 0.1:
        y = 0
    elif angle == 30 or angle == 0.15:
        y = 1
    elif angle == 45 or angle == 0.2:
        y = 2
    elif angle == 60 or angle == 0.22:
        y = 3
    elif angle == 75 or angle == 0.27:
        y = 4
    elif angle == 90 or angle == 0.3:
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
def turbinesW(product_line, meters):
    x = int((meters / 10) - 2)
    if product_line == 'meh' or product_line == 0.83:
        y = 0
    elif product_line == 'good' or product_line == 0.86:
        y = 1
    elif product_line == 'fine' or product_line == 0.89:
        y = 2
    elif product_line == 'super' or product_line == 0.92:
        y = 3
    elif product_line == 'mondo' or product_line == 0.94:
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
bends = [20,30,45,60,75,90]
#turbines = ['meh','good','fine','super','mondo']
turbines = [0.83,0.86,0.89,0.92,0.94]

effective_performance_ratings = [x for x in range(20, 130, 10)]
internal_diameters = [x/4.0 for x in range(0,13)]
internal_diameters[0] = 0.1

def systemEfficiency(np,nt,h,f,lu,ld,eee,d):
    num = np*((2*nt*gravity*h)-(f*pow(ld,3)*pow(pi,2)*pow(d,3)/16)-(pow(pi,2)*eee*pow(d,4)*pow(ld,2)/16))
    den = (2*gravity*h)-((pow(pi,2)/16)*f*pow(d,3)*(pow(lu,3))-((pow(pi,2)/16)*eee*pow(d,4)*pow(lu,2))
    return 120*num/den

max = 0
for pump in pumps:
    for pipe in pipes:
        for bend in bends:
            for turbine in turbines:
                for m in effective_performance_ratings:
                    for d in internal_diameters:
                        value = systemEfficiency(pump,turbine,m,pipe,75,75,bendFittings(bend,d),d)
                        if value > max:
                            max = value
                            print(round(max,3))
                            print(pump,pipe,bend,turbine,m,d)
