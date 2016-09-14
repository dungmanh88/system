#!/usr/bin/python3
from sys import argv
script, filename = argv

print("We are going to read the file", filename)
with open(filename) as target:
  line = target.readline()
  while line:
    print(line, end='')
    line = target.readline()
target.close()
