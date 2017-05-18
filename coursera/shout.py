filename = raw_input("Enter your file: ")
try:
    fd = open(filename)
except:
    print "There is no %s" % filename
    quit()

for line in fd:
    print line.rstrip().upper()
