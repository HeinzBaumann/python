# exercise 1
# Defining and calling a function
# Conditions, if, elif, else
# Handling erros

# this is a function
# extend the function to take an argument and based on the given number print for 0 Hello, 
# for 1 Bonjour, all other numbers Undefined
# on the given numver 1 
def myFunction():
    print("Hello")

myFunction()
#myFunction(0)
#myFunction(1)
#myFunction(2)

# handling errors
try:
    myFunction(i)  # i is not defined, it will throw an error
except:
    print("Error handler: error in function call")