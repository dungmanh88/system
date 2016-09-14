from sys import argv

script, input_file = argv

def print_all(f):
  print(f.read())

def rewind(f):
  f.seek(0)

def print_a_line(line_number, f):
  print (line_number, f.readline(), end='')

current_file = open(input_file)

print("Let print the whole file")

print_all(current_file)

print("rewind to the start")

rewind(current_file)

print("print three lines")

for i in range(0, 3):
  print_a_line(i, current_file) 
