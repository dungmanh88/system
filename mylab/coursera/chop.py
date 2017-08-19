def initList(t):
    t.append("Attack on titan")
    t.append("Alien")
    t.append("I am robot")
    t.append("Himura Kenshin")

def chop(t):
    del t[0]
    t.pop()

theList = list()
initList(theList)

chop(theList)
print theList

def middle(t):
    return t[1:len(t)-1]

theList = list()
initList(theList)
print theList
print middle(theList)
