#!/usr/bin/python3
import math as m
name = "ManhDung"
age = 28
print("My name is", name, ". I am", age)
print("My name is %s. I am %d" % (name, age))
print("My name is {}. I am {}".format(name, age))
print("My name is {0}. I am {1}".format(name, age))
print("My name is {name}. I am {age}".format(name=name, age=age))

bookList = [ ("Ken Kesey", "Bay tren to chim cuc cu", 4), ("Paul Coelho", "Nha gia kim", 5), ("Salinger", "Bat tre dong xanh", 5)]

for author, book, star in bookList:
    print("The book \'{0}\' of {1} got {star:5d} star".format(book, author, star=star))

bookList = { "Bay tren to chim cuc cu": 4, "Nha gia kim": 5, "Bat tre dong xanh": 5}
count=1
for book, star in bookList.items():
    print("{0:3d}. The book \'{book}\' got {star:5d} star".format(count, book=book, star=star), end="")
    count += 1
print("")
print("The value of PI = {0:5f}".format(m.pi))
