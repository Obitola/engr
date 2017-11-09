import matplotlib.pyplot as plt
from math import floor

file = input('Input the name of the file:')
try:
    lines = list(open(file, 'r'))
except FileNotFoundError:
    lines = []
except IOError:
    lines = []
except PermissionError:
    lines = []

count = 0
a_data = [0]
for x in range(0,len(lines)):
    if count % 10 == 0 and count > 0:
        a_data.append(0)
    a_data[int(floor(count / 10))] += float(lines[x]) / 10.0
    count += 1

print(a_data)
v_data = []
v_data.append(a_data[0])
for x in range(1, len(a_data)):
    v_data.append(v_data[x - 1] + a_data[x])

x_data = []
x_data.append(v_data[0])
for x in range(1, len(v_data)):
    x_data.append(x_data[x - 1] + v_data[x])

print(v_data)
print(x_data)