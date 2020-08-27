#!/usr/bin/python3

x_list = [1,2,3]
y_list = [5,9,1]

## Wehnever we have two or more list, and we have to walk through it at the same time,
##       we use zip
#the bad way
for i in range(len(x_list)):
    x = x_list[i]
    y = y_list[i]
    print(x, y)

# the good way
for x, y in zip(x_list, y_list):
    print(x, y)

# Scenerio2
# Swap two values
the bad way
x = 10
y = -10
print("Before x:{} and y:{}".format(x,y))
tmp = y
y = x
x = tmp
print("After x:{} and y:{}".format(x,y))

#The good way

x = 10
y = -10
print("Before x:{} and y:{}".format(x,y))
x , y = y , x
print("After x:{} and y:{}".format(x,y))

# Scenerio 3
#
#The bad way
ages = { 'Mary': 31 , 
         'Jhon': 28,
         'Dick': 58
         }
if "Dick" in ages:
    age = ages['Dick']
else:
    age = "Unknown"

print("Dick is {} years old".format(age))

#The goodway
age = ages.get("Dick","Unknown")
print("Dick is {} years old".format(age))


# Scenerio 4
needle = "a"
haystack = ["a","b","c"]

#the bad way
found = False
for letter in haystack:
    if needle == letter:
        print("Found")
        found = True
        break
if not found:
    print("Not Found!")

#The good way
for letter in haystack:
    if needle == letter:
        print("Found")
        found = True
        break
else: #if no break occured, execute else
    print("Not Found!")

# Scenerio 5
# File reading

#the bad way
f = open('file.txt')
text = f.read()
for line in text.split("\n"):
    print(line)
f.close()

#the good way
with open('file.txt') as f:
    for line in f:
        print(line)

## Scenerio 6

print("Converting")
try:
    print(int('X'))
except:
    print("Conversion Failed")
else:
    print("Conversion Successful")
finally:
    print("DONE")