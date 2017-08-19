str = raw_input("Enter a string: ")
index = len(str) - 1
while index > -1:
    print str[index]
    index = index - 1
print "Done"

print "Other method"

str = str[::-1]
for char in str:
    print char
print "Done2"
