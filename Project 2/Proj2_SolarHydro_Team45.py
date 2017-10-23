from math import pow, pi

#given
energy_out = 120
gravity = 9.81
water_density = 1000

# #inputs
# pump_efficiency = input("Enter your pump efficiency:")
# turbine_efficiency = input("Enter your turbine efficiency:")
# pipe_diameter = input("Enter your pipe diameter:")
# pipe_length = input("Enter your pipe length:")
# pipe_friction_factor = input("Enter your pipe's friction coefficient:")
# reservoir_depth = input("Enter the reservoir's depth:")
# bottom_reservoir_elevation = input("Enter the bottom reservoir's elevation:")
# flow_rate_pump = input("Enter the flow rate of the pump:")
# flow_rate_turbine = input("Enter the flow rate of the turbine:")
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
def energyTurbine(energy_out,turbine_efficiency):
    return energy_out * (1 / turbine_efficiency - 1)

def pipeFrictionDown(water_mass, pipe_friction_factor, pipe_length, velocity_down, pipe_diameter):
    return water_mass * (pipe_friction_factor * pipe_length * pow(velocity_down, 2) / (2 * pipe_diameter))

def energyLossHitting(water_mass, velocity_down):
    return water_mass * pow(velocity_down, 2) / 2

def massWater(water_density, flow_rate_pump, fill_time, pipe_length, pipe_diameter):
    return water_density * pi * pow()


