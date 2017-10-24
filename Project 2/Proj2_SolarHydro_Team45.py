#given
energy_out = 120
gravity = 9.81
water_density = 1000

#inputs
pump_efficiency
turbine_efficiency
pipe_diameter
pipe_length
pipe_friction_factor
reservoir_depth
bottom_reservoir_elevation
flow_rate_pump
fluid_velocity_up
fluid_velocity_down
flow_rate_turbine
bend_coefficient_1
bend_coefficient_2

#outputs
reservoir_surface_area
energy_in
system_efficiency
fill_time
empty_time

#other variables



#functions needed
def energyTurbine(energy_out,turbine_efficiency):
    return energy_out * (1 / turbine_efficiency - 1)

def massWater(water_density, flow_rate_pump, fill_time, pipe_length, pipe_diameter): 
    return water_density * pi * pow((pipe_diameter/2), 2)* pipe_length 

def energyPipeFrictionUp(pipe_friction_factor, massWater, pipe_length, fluid_velocity_up, pipe_diameter): 
    return (massWater*pipe_friction_factor*pipe_length*pow(fluid_velocity_up,2))/(2*pipe_diameter) 
 
def energyPipeFrictionDown(pipe_friction_factor, massWater, pipe_lenth, fluid_velocity_up, pipe_diameter): 
    return(massWater*pipe_friction_factor* pipe_length*pow(fluid_velocity_down,2))/(2*pipe_diameter) 

def energyPumpLoss(pump_efficiency, energy_in): 
    return (1-pump_efficiency)/energy_in 

def energyTurbineLoss(energy_out, turbine_efficiency):     
    return energy_out*(1/(turbine_efficiency-1)) 

def volumetricFlowUp(pipe_diameter, fluid_velocity_up) 
    return pow((pipe_diameter/2),2)*pi*fluid_velocity_up

def volumetricFlowDoown(pipe_diameter, fluid_velocity_down)
    return pow((pipe_diameter/2),2)*pi*fluid_velocity_down
