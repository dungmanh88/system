numList = [];
while True:
    try:
        inp = raw_input("Enter a number: ");
        if inp == "done":
            break;
        print "inp = " + str(inp)
        inp = float(inp)
        numList.append(inp)
    except:
        print "Invalid input"
for i in numList:
    print i
if len(numList) > 0:
    print sum(numList), len(numList), sum(numList)/float(len(numList)), max(numList), min(numList)

largest = None
smallest = None
while True:
    num = raw_input("Enter a number: ")
    if num == "done" : break
    try:
        num = float(num)
    except:
        print "Invalid input"
        continue
    if largest == None or largest < num:
        largest = num
    if smallest == None or smallest > num:
        smallest = num

print "Maximum is", largest
print "Minimum is", smallest
