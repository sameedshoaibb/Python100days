#!/usr/bin/python3

""" start """

array = []

def INPUT(value):
    print("Yalla!"+str(value))
    for i in range(0, value):
        TAKE_INPUT2 = eval(input("Enter the number"))
        array.append(TAKE_INPUT2)
    calculate(array)


def calculate(val):
    sum1 = 0
    for d in val:
        sum1 += d + sum1 
    print(sum1/TAKE_INPUT)

TAKE_INPUT = eval(input("Enter the number of elements to be inserted:"))
print(INPUT(TAKE_INPUT))