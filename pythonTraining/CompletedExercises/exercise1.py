# Defining and calling a function
# Conditions, if, elif, else
# Handling erros

# this is a function
def myFunction(i):
    if i == 0:
        print("Hello")
    elif i == 1:
        print("Bonjour")
    else:
        print("Undefined")

myFunction(0)
myFunction(1)
myFunction(2)

# handling errors
try:
    myFunction(i)  # i is not defined, it will throw an error
except:
    print("Error handler: error in function call")