# simple calculator
# Conditions, if, elif, else
# user input
# variable

intStack = 0
intInput = 0
strOperator = ''

while (True):
    str = input()
    if str == '+' or str == '-' or str == '*' or str == '/':
        strOperator = str
    elif str.isnumeric():
        intInput = int(str)
        if strOperator == '+':
            intStack += intInput
        elif strOperator == '-':
            intStack -= intInput
        elif strOperator == '*':
            intStack = intInput * intStack
        elif strOperator == '/':
            intStack = intStack / intInput
        else:
            intStack = intInput
        print('\t', intStack)
    elif str == 'q' or str == 'quit':
        print("terminated")
        break
    else:
        print("error")
        break



