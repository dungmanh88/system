def counter(str, letter):
    counter = 0
    for char in str:
        if char == letter: counter = counter + 1
    return counter

str = raw_input("Enter a string: ")
letter = raw_input("Enter a letter: ")

print "Counter: ", counter(str, letter)

print "Counter using built-in method: ", str.count(letter)
