# exercise 3
# Tuple, List
# while loops 
# user input usng input()
#

helloTuple = ("Hello", "Bonjour", "Hallo", "Ciao", "Hola", "Aloha", "Kaohe")
#helloList = ["Hello", "Bonjour", "Hallo", "Ciao", "Hola", "Aloha", "Kaohe"]

# this is a function
def myFunction(i):
    try:
        print(helloTuple[i])
    except:
        print("Error: out of range")

try: 
    while 1:
        str = input()
        if str == "exit":
            break
        try:
            i = int(str)
        except: 
            print("Invalid Input")
            continue
        if i == -1:
            break
        else:
            myFunction(i)
except:
    print("Error in calling myFunction")