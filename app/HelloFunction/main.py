#!/usr/bin/python3

def print_three(*args):
  arg1, arg2, arg3 = args
  print ("arg1:", arg1, "arg2:", arg2, "arg3:", arg3)

def print_two(arg1, arg2):
  print("arg1:", arg1, "arg2:", arg2)

logic = "the truth"
def fake(logic):
  logic = "the false"
  print("Change to", logic)
fake(logic)
print (logic)

print_three("foo", "bar", "seen")
print_two("angel", "daemon")
