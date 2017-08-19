import sys
import os

if len(sys.argv) != 3:
    print "1- Usage %s %s %s" % (sys.argv[0], "Old filename", "New filename")
    sys.exit()

old_fname = sys.argv[1]
new_fname = sys.argv[2]

if old_fname.strip() == "" or new_fname.strip() == "":
    print "2- Usage %s %s %s" % (sys.argv[0], "Old filename", "New filename")
    sys.exit()

os.rename(old_fname, new_fname)
