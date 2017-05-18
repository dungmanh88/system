filename = raw_input("Enter your filename: ")
wordList = list()
try:
    fd = open(filename)
except:
    print "File not found %s" % filename
    quit()
for line in fd:
    if len(line) == 0: continue
    for word in line.rstrip().split():
        if word not in wordList:
            wordList.append(word)
print sorted(wordList)
