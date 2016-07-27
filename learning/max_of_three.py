a = int(raw_input("Enter first number: "))
b = int(raw_input("Enter second number: "))
c = int(raw_input("Enter third number: "))

def max_of_two(a, b):
    return a < b and b or a 

def max_of_three(a, b, c):
    return max_of_two(max_of_two(a ,b), c)	

print "Max number in %d %d %d is %d" % (a, b ,c, max_of_three(a, b, c))
