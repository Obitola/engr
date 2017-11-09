import matplotlib.pyplot as plt
from math import sqrt

def calculate_w(l, c):
    return 1 / sqrt(l * c)
file = input('Input the name of the file:')
try:
    lines = list(open(file, 'r'))
except FileNotFoundError:
    lines = []
except IOError:
    lines = []
except PermissionError:
    lines = []

for x in range(len(lines)):
    count = 0
    while not lines[x][count] == ' ':
        count += 1
    lines[x] = lines[x][1:count-1]

l = float(lines[0])
c_values = []
for x in range(1, len(lines)):
    c_values.append(float(lines[x]))

c_values.sort()
w_values = [calculate_w(l,c) for c in c_values]

plt.figure(1)
plt.plot(c_values, w_values)
plt.title('Circut Analysis')
