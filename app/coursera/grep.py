import re

pattern = raw_input("Enter your pattern: ")
filename = raw_input("Enter a file: ")
try:
    fd = open(filename)
except:
    print "File not found %s" % filename
    quit()
match = 0
for line in fd:
    line = line.rstrip()
    if re.search(pattern, line): match = match + 1

print "%s had %d lines that matchd %s" % (filename, match, pattern)
