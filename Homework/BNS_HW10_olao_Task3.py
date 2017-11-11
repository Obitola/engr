import matplotlib.pyplot as plt
from math import sqrt

def calculate_w(l, c):
    return 1 / sqrt(l * c)

def get_contents_of_file(filename):
    try:
        lines = list(open(filename, 'r'))
    except FileNotFoundError:
        print('Error: File not found')
        lines = []
    except IOError:
        print('Error: This file is currently being used')
        lines = []
    except PermissionError:
        print('Error: You do not have permission to access this file')
        lines = []
    
    return lines

lines = get_contents_of_file('numbers.txt')
print(lines)
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