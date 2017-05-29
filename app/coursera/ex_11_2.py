import re
filename = raw_input("Enter a file: ")
try:
    fd = open(filename)
except:
    print "File not found %s" % filename
    quit()
revision_list = list()
for line in fd:
    line = line.rstrip()
    revision = re.findall('^New Revision:\s([0-9]+)$', line)
    revision_list.extend(revision)

print sum([int(i) for i in revision_list])/float(len(revision_list))
