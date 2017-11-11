#file = str(input('Enter name of file:'))

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