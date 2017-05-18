def get_sum(a,b):
    if a == b:
        return a
    l = [a,b]
    l.sort()
    i=l[0]
    while i < l[1]-1:
        i = i + 1
        l.append(i)
    return sum(l)
