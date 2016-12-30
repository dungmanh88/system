def add(a, b):
  print("ADDING {0} + {1}".format(a,b))
  return a+b

def substract(a, b):
  print("SUBSTRACTING {0} - {1}".format(a, b))
  return a-b

def multiply(a, b):
  print("MULTIPLYING {0} * {1}".format(a,b))
  return a*b

def divide(a, b):
  print("DIVIDING {0} / {1}".format(a,b))
  return a/b

print("Let's do some calculation")
age = add(20, 8)
height = substract(177,7)
weight = multiply(8,8)
iq = divide(100,2)

print ("Age: {0:d}, Height: {1:d}, Weight: {2:d}, Iq = {3:f}".format(age,height, weight, iq))
print("Here is a puzzle")

what = add(age, substract(height, multiply(age, divide(iq,weight))))
print("Can you guess  ? ")

print ("Final result = {:f}".format(what))


