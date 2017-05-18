filename = raw_input("Enter your filename: ")
try:
    fd = open(filename)
except:
    print "File not found %s" % filename
    quit()

count = 0
for line in fd:
    words = line.rstrip().split()
    if len(words) == 0 or words[0] != "From" or words[0][-1] == ":" or len(words) < 2: continue
    mail = words[1]
    count = count + 1
    print mail

print "There were %d lines in the file with From as the first word" % count
