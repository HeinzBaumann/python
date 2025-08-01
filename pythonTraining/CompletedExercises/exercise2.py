# exercise 2
# command line parameters 
# if, else, match
# handling errors

import sys

# Debug outputs
#print("Script name:", sys.argv[0])
#print(sys.argv)

myValue = -2
if len(sys.argv) > 1:
    if len(sys.argv) == 2:
        try:
            myValue = int(sys.argv[1])
        except: 
            myValue = -1
    else:
        myValue = -1

# this is a function
def myFunction(i):
    match i:
        case 0:
            print("Hello")
        case 1:
            print("Bonjour")
        case 2:
            print("Aloha")
        case -2:
            print("Missing argument. Syntax: python3", sys.argv[0], "<number>")
        case _:
            print("Error in myFunction: Invalid value: ", f'{i}')

# error handling
try: 
    myFunction(myValue)
except:
    print("Error in calling myFunction")