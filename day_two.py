""" Yalla Sameed"""

""" Objective: To create a Program which will check whether the file exists or not.
                If it is not exists, it will create the file  """

#!/usr/bin/python3
import os
FILE_NAME = "file.py6"
PATH = "/home/sameed-shoaib/test/"+FILE_NAME

def create_directory():
    """ To create a dynamic File """
    var_i = 1
    try:
        while var_i < 2:
            os.mkdir(PATH)
            print("The file has been created")
            var_i += 1
    except OSError:
        print("There is an OS error")


def check_directory():
    """ To check whether File's exist or not """
    if not os.path.exists(PATH):
        print("FILE DO NOT EXISTS")
        create_directory()
        print("Creating new file")
    else:
        print("The file already exists")

# Main Function
try:
    check_directory()
except OverflowError as e_e:
    print("e")
else:
    print("Wonderful. The code is executed sucessfully")
