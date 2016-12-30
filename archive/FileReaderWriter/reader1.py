#!/usr/bin/python3
from sys import argv
script, filename = argv

print("We are going to read the file", filename)
target = open(filename, "r")
print(target.read(), end='')
target.close()
