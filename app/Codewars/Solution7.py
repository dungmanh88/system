def duplicate_encode(word):
    #your code here
    result, word = "", word.lower()
    for c in word:
        if word.count(c) == 1: result = result + "("
        else: result = result + ")"
    return result

def duplicate_encode(word):
    #your code here
    word = word.lower()
    return "".join('(' if word.count(c) == 1 else ')' for c in word)


#This solution is O(n) instead of O(n^2) like the methods that use .count()
#because .count() is O(n) and it's being used within an O(n) method.
#The space complexiety is increased with this method.
import collections
def duplicate_encode(word):
    new_string = ''
    word = word.lower()
    #more info on defaultdict and when to use it here:
    #http://stackoverflow.com/questions/991350/counting-repeated-characters-in-a-string-in-python
    d = collections.defaultdict(int)
    for c in word:
        d[c] += 1
    for c in word:
        new_string = new_string + ('(' if d[c] == 1 else ')')
    return new_string

def duplicate_encode(word):
    new_string = ''
    word = word.lower()
    #more info on defaultdict and when to use it here:
    #http://stackoverflow.com/questions/991350/counting-repeated-characters-in-a-string-in-python
    d = {}
    ## init d
    for c in word:
        d[c] = 0
    ## increment d
    for c in word:
        d[c] += 1
    ## using d
    for c in word:
        new_string = new_string + ('(' if d[c] == 1 else ')')
    return new_string
