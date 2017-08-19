filename = raw_input("Enter your filename: ")
if filename == "na na boo boo":
    print "NA NA BOO BOO TO YOU - You have been punk'd!"
    quit()
try:
    fd = open(filename)
except:
    print "File cannot be opened: %s" % filename
    exit()

count_line = sum(1 for line in fd)
print "There were %d subject lines in %s" % (count_line, filename)
