import sys

def sum_two_smallest_numbers(numbers):
    a, b = sys.maxsize, sys.maxsize
    for i in numbers:
        if a > i:
            a = i
    for j in numbers:
        if a == j:
            continue
        if b > j:
            b = j
    return a+b

def sum_two_smallest_numbers(numbers):
    smallest1 = min(numbers)
    numbers.remove(smallest1)
    smallest2 = min(numbers)
    return smallest2 + smallest1
