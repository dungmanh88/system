t = list()
while True:
    ip = raw_input("Enter a number: ")
    if ip == "done": break
    try:
        number = float(ip)
    except:
        print "Something is wrong"
        continue
    t.append(number)
print "Maximum:", max(t)
print "Minimum:", min(t)
