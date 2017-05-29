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
    asterisk_pos = mail.find("@")
    domain = mail[asterisk_pos+1:]
    theDict[domain] = theDict.get(domain, 0) + 1
print theDict
