import sys

with open(sys.argv[1], "r") as f:
    for lines in f:
        print lines
    f.close()

with open(sys.argv[1], "a+") as f:
    f.write("Hello world\n")
    f.close()
