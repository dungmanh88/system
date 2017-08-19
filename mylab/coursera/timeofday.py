filename = raw_input("Enter your file name: ")
try:
    fd = open(filename)
except:
    print "File not found: %s" % filename
    quit()

theDict = dict()

for line in fd:
    words = line.split()
    if len(words) < 1 or words[0] != "From" or words[0][-1] == ":" or len(words) < 6: continue
    time = words[5]
    time_split = time.split(":")
    if len(time_split) < 1: continue
    hour = time_split[0]
    theDict[hour] = theDict.get(hour, 0) + 1

result = theDict.items()
result.sort()
for hour, count in result:
    print hour, count
