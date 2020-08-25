#!/usr/bin/python3

def get_answer(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in("yes", "no","maybe"):
            return answer

print(get_answer("yes or no"))
