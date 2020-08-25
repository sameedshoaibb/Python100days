#!/usr/bin/python3
'''
# Put most code in  function
# use __name__ to control execution of your code
# create a function called __main__ to containt the code you want to run
# Call other function from main
'''

from time import sleep
print("This is my file to demonstrate the best practice")

def write_data_to_database(data):
    ''' Fucntion to write in the database '''
    print("Writing data to the database")
    print(data)

def process_data(data):
    ''' Fucntion to process in the database '''
    print("Beginning the data processing...")
    modified_data = data + "that has been modifed"
    sleep(1)
    print("Data processing has been finished")
    return modified_data

def read_data_from_web():
    ''' Fucntion to read from the web '''
    print("Reading data from the web")
    data = "Data from the web"
    return data

def main():
    ''' Beginning of the Function Logic '''
    data = read_data_from_web()
    modified_data = process_data(data)
    write_data_to_database(modified_data)

if __name__ == "__main__":
    main()
# Condition evaluate to ture when name = main, MAIN means python executer is executing your
#  script and not importing it