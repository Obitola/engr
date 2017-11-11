import matplotlib.pyplot as plt
from math import pow, sin, cos, sqrt, pi

g = 9.8
d = 0.75
theta = 53.13 * pi / 180
k = 1000
friction_coefficient = 0.3
m = 5

#def works(theta, friction_coefficient):
#    a = 0.5 * k
#    b = m * g * (cos(theta) * friction_coefficient - sin(theta))
#    c = d * m * g (cos(theta) * friction_coefficient - sin(theta))
#    if pow(b, 2) > 4 * a * c:
#        return True
#    else:
#        return False

def calculate_deflection(d, theta, k, friction_coefficient, m):
    a = 0.5 * k
    b = m * g * (cos(theta) * friction_coefficient - sin(theta))
    c = d * m * g * (cos(theta) * friction_coefficient - sin(theta))
    try:
        return (-b + sqrt(pow(b, 2) - 4 * a * c))/(2 * a)
    except:
        return 0
#task 1
d_range = [x / 10.0 for x in range(0,11)]
deflection = []
for d in d_range:
    deflection.append(calculate_deflection(d, theta, k, friction_coefficient, m))
plt.figure(1)
plt.plot(d_range, deflection)
plt.title('Deflection vs Distance')
plt.xlabel('Distance (m)')
plt.ylabel('Deflection (m)')
plt.grid()


d = 0.75
#task 2
theta_range = [(x / 10.0) * pi / 180 for x in range(180, 901)]
deflection = []
for theta in theta_range:
    deflection.append(calculate_deflection(d, theta, k, friction_coefficient, m))
plt.figure(2)
plt.plot(theta_range, deflection)
plt.title('Deflection vs Angle')
plt.xlabel('Angle (rad)')
plt.ylabel('Deflection (m)')
plt.grid()


theta = 53.13 * pi / 180
#task 3
k_range = range(50, 5050, 50)
deflection = []
for k in k_range:
    deflection.append(calculate_deflection(d, theta, k, friction_coefficient, m))
plt.figure(3)
plt.plot(k_range, deflection)
plt.title('Deflection vs k')
plt.xlabel('k (no units)')
plt.ylabel('Deflection (m)')
plt.grid()


k = 1000
#task 4
friction_coefficient_range = [float(x) / 10.0 for x in range(0, 13, 2)]
deflection = []
for fc in friction_coefficient_range:
    deflection.append(calculate_deflection(d, theta, k, fc, m))
plt.figure(4)
plt.plot(friction_coefficient_range, deflection)
plt.title('Deflection vs Friction Coefficient')
plt.xlabel('Friction Coefficient (no units)')
plt.ylabel('Deflection (m)')
plt.grid()


#task 5
m_range = [x / 10.0 for x in range(10,251,5)] #todo: fix
deflection = []
for m in m_range:
    deflection.append(calculate_deflection(d, theta, k, friction_coefficient, m))
plt.figure(5)
plt.plot(m_range, deflection)
plt.title('Deflection vs Mass')
plt.xlabel('Mass (kg)')
plt.ylabel('Deflection (m)')
plt.grid()