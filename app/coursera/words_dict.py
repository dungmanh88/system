import random
import string

def generateRandomString():
    size = 6
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))

filename = raw_input("Enter your file name: ")
try:
    fd = open(filename)
except:
    print "File not found: %s" % filename
    quit()

theDict = dict()
for line in fd:
    if len(line) < 1: continue
    words = line.split()
    for word in words:
        theDict[word] = generateRandomString()

for key in theDict.keys():
    print "%s: %s" % (key, theDict[key])
