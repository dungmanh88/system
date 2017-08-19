txt = 'but soft what light in yonder window breaks'
words = txt.split()
t = list()
print repr(t)
for word in words:
    t.append((len(word), word))
print t
t.sort(reverse=True)
print t
res = list()
for length, word in t:
    print length
    res.append(word)
print res
