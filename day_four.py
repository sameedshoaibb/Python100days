#!/usr/bin/python3

""" start """


TAKE_INPUT = eval(input("Enter the number of elements to be inserted:"))
array = []
for i in range(0, TAKE_INPUT):
    TAKE_INPUT2 = eval(input("Enter the number"))
    array.append(TAKE_INPUT2)

def sumer(val):
    print("SAMEED"+ val)

print(sumer(array)/len(array))