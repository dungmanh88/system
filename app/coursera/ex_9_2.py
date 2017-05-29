filename = raw_input("Enter your file name: ")
try:
    fd = open(filename)
except:
    print "File not found: %s" % filename
    quit()

theDict = dict()

for line in fd:
    words = line.split()
    if len(words) < 1 or words[0] != "From" or words[0][-1] == ":" or len(words) < 3: continue
    day = words[2]
    theDict[day] = theDict.get(day, 0) + 1

print theDict
