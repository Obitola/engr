import matplotlib.pyplot as plt
from math import pow, sin, cos, sqrt, pi

g = 9.8
d = 0.75
theta = 53.13 * pi / 180
k = 1000
friction_coefficient = 0.3
m = 5

def works(theta, friction_coefficient):
    if sin(theta) - friction_coefficient * cos(theta) >= 0:
        return True
    else:
        return False

def calculate_deflection(d, theta, k, friction_coefficient, m):
    return sqrt((2 * m * g * d * (sin(theta) - friction_coefficient * cos(theta))) / k)




#task 1
d_range = [x / 10.0 for x in range(0,11)]
deflection = []
for d in d_range:
    if works(theta, friction_coefficient):
        deflection.append(calculate_deflection(d, theta, k, friction_coefficient, m))
plt.figure(1)
plt.plot(d_range, deflection)

#task 2
theta_range = [(x / 10.0) * pi / 180 for x in range(180, 901)]
deflection = []
for theta in theta_range:
    if works(theta, friction_coefficient):
        deflection.append(calculate_deflection(d, theta, k, friction_coefficient, m))
plt.figure(2)
plt.plot(theta_range, deflection)

#task 3
k_range = range(50, 5050, 50)
deflection = []
for k in k_range:
    if works(theta, friction_coefficient):
        deflection.append(calculate_deflection(d, theta, k, friction_coefficient, m))
plt.figure(3)
plt.plot(k_range, deflection)

#task 4
friction_coefficient_range = [x / 10.0 for x in range(0, 13, 2)]
deflection = []
for friction_coefficient in friction_coefficient_range:
    if works(theta, friction_coefficient):
        deflection.append(calculate_deflection(d, theta, k, friction_coefficient, m))
plt.figure(4)
plt.plot(friction_coefficient_range, deflection)

#task 5
m_range = [x / 10.0 for x in range(10,251,5)] #todo: fix
deflection = []
for m in m_range:
    if works(theta, friction_coefficient):
        deflection.append(calculate_deflection(d, theta, k, friction_coefficient, m))
plt.figure(5)
plt.plot(m_range, deflection)
