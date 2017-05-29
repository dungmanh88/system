import re
try:
    print sum( [ int(i) for i in re.findall('[0-9]+',open(raw_input("Enter a file name: ")).read()) ] )
except:
    print "File not found"
