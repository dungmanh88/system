filename = raw_input("Enter your file name: ")
try:
    fd = open(filename)
except:
    print "File not found: %s" % filename
    quit()

theDict = dict()

for line in fd:
    words = line.split()
    if len(words) < 1 or words[0] != "From" or words[0][-1] == ":" or len(words) < 2: continue
    mail = words[1]
    theDict[mail] = theDict.get(mail, 0) + 1

result = list()
for email, count in theDict.items():
     result.append((count, email))

result.sort(reverse=True)

print result

email, count = result[0]
print email, count
