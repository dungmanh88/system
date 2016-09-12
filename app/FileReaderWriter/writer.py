#!/usr/bin/python3
from sys import argv

script, filename = argv

print("This script is", script)
print("We are going to overwrite", filename)
input("?")
print("Opening the file...")
target = open(filename, "w")
print("Erase file ", filename)
target.truncate()

print("Enter three lines")
lines = ()
for i in range(0, 3):
  print("line", i + 1, ": ", end='')
  line = input()
  lines += (line,)
print(lines)
print("I am going to write these to the file")

target.write("\n".join(lines) + "\n")

print("Close it")
target.close()
