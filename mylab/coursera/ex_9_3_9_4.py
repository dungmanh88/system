filename = raw_input("Enter a file name: ")
try:
    fd = open(filename)
except:
    print "File not found: %s" % filename
    quit()

theDict = dict()

for line in fd:
    words = line.rstrip().split()
    if len(words) < 1 or words[0] != "From" or words[0][-1] == ":" or len(words) < 2: continue
    mail = words[1]
    theDict[mail] = theDict.get(mail, 0) + 1
    top_message = max(theDict.values())
    if theDict[mail] == top_message:
        top_mail = mail
print theDict
print top_mail, top_message
