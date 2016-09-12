#!/usr/bin/python3
from sys import argv
script, filename = argv

print("We are going to read the file", filename)
target = open(filename, "r")
line = target.readline()
while line:
  print(line, end='')
  line = target.readline()
target.close()
