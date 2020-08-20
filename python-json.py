#!/usr/bin/python3

import json
import requests

REQUEST = requests.get("https://jsonplaceholder.typicode.com/posts/1/comments")
DATA_IN = REQUEST.content

DATA = json.loads(DATA_IN) #making python object

EMAIL_IDS = dict()

for i in DATA:
    ID = i["id"]
    EMAIL = i["email"]
    print(ID,EMAIL)
    EMAIL_IDS[EMAIL] = ID


print("Email id number is", EMAIL_IDS['Lew@alysha.tv'])
#print(json.dumps(DATA, indent = 2))    # convert into JSON:
#The dump() method is used when the Python objects have to be stored in a file.
# print(DATA)

# data = json.loads(source)
# print(data)