#!/usr/bin/python3 

''' Playing with json '''

import json

with open('data.json', 'r') as f:
    DATA_STORE = json.load(f)

print(DATA_STORE["office"])
