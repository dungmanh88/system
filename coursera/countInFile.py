def countWordInString(string, word):
    index = 0
    count = 0
    while True:
        stopFindingIndex = string.find(word, index)
        if stopFindingIndex > 0:
            count = count + 1
            index = stopFindingIndex + len(word)
        else:
            break
    return count

filename = raw_input("Enter the full path to file: ")
word = raw_input("Enter a word for searching: ")
fhand = open(filename)
countWord = 0
for line in fhand:
#    countWord = countWord + countWordInString(line, word)
    line = line.rstrip()
    if line.startswith(word):
        print line

print "Total word: %d" % countWord
