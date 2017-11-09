file = input('Enter name of file:')
try:
    lines = list(open(file, 'r'))
except FileNotFoundError:
    lines = []
except IOError:
    lines = []
except PermissionError:
    lines = []


print(lines)