filename = raw_input("Enter your filename: ")

try:
    fd = open(filename)
except:
    print "There is no file %s exsist" % filename
    exit()

count, total = 0, 0

for line in fd:
    if line.startswith("X-DSPAM-Confidence:"):
        total = total + float(line[line.find(":") + 1:].lstrip())
        count = count + 1

print "Avegare: ", total/count
