fhandle = open("mbox-short.txt");
count = 0
for line in fhandle:
    count = count + 1
fhandle.close()
print "Total line %d" % count
