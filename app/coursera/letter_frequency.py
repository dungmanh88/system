import string

filename = raw_input("Enter your file name: ")
try:
    fd = open(filename)
except:
    print "File not found: %s" % filename
    quit()

theDict = dict()
#deleteChars = string.punctuation + string.digits + "\t" + " "
for line in fd:
    line = line.rstrip()
    if len(line) < 1: continue
    line = line.lower()
    #line = line.translate(None, deleteChars)
    chars = list(line)

    #print "### ", chars

    for char in chars:
        if char in string.ascii_lowercase:
            theDict[char] = theDict.get(char, 0) + 1

result = list()

for letter, count in theDict.items():
    result.append((count, letter))

result.sort(reverse=True)

for count, letter in result:
    print letter, count
