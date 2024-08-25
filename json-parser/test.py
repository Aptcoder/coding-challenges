import sys


with open('./test.txt') as fd:
    file = fd.read()
    for char in file:
        print('char', repr(char))