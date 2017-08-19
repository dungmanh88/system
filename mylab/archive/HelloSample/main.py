#!/usr/bin/python3

from random import sample
words = ["dont't count your chicken before they are hatched", "somebody walked over my grave", "final fantasy", "linux mint"]

def generate_random_word():
  print (sample(words,1)[0])

if __name__ == '__main__':
  generate_random_word()


