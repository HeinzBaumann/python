# Exercise 4
# Lists, Dictionaries
# functions
# sorting lists
# for ... in ...
# formating output
# calculations

# Our dictionary schema:
#  { "lastName": "", "firstName": "", "title": "", 
#    "started": "", "location": "", "management": False }

myEmloyeeList = [{ "lastName": "Baumann", "firstName": "Heinz", "title": "Contractor", "started": "01/01/2023", "location": "home", "management": False},
                 { "lastName": "Vagner", "firstName": "Ninon", "title": "Director", "started": "01/01/2022", "location": "Brussels", "management": True},
                 { "lastName": "Siddaq", "firstName": "Hasan", "title": "Employee", "started": "01/01/2024", "location": "Brussels", "management": False},
                 { "lastName": "Gagliardi", "firstName": "Lucio", "title": "Contractor", "started": "05/01/2025", "location": "home", "management": False},
                 { "lastName": "Bouali", "firstName": "Tawfik", "title": "Employee", "started": "01/01/2022", "location": "Brussels", "management": False},
                 { "lastName": "Pappalardo", "firstName": "Giuseppe", "title": "Employee", "started": "01/01/2022", "location": "Brussels", "management": False}
                ]

# support functions
def pct(num1, num2):
    return (num1 / num2) * 100

# sort function to sort the empoyee list by last name
def sortFunc(e):
    return e["lastName"]

# sort the employee list using the sort function as the key
myEmloyeeList.sort(key=sortFunc)

# print out all emmployee data (name, first name, title) in CSV format
outStr = "Last name,First name,Tite,Start Date,Location,Manager\n"
for dictx in myEmloyeeList:
    dictLength = len(dictx)
    i = 0
    for item in dictx:
        outStr += str(dictx[item])
        i += 1
        if i < dictLength:  # skip output of ',' for the last item
            outStr += (',')
    outStr += ('\n')

print(outStr)

def listManagers(myList):
# output lastName, firstName, title and location of all employees in managements
    outStr = "Total employees in management:"
    outStr2 = "List of managers:\n"
    cnt = 0
    for dictx in myList:
        if dictx.get("management") == True:
            cnt += 1
            outStr2 += str(dictx.get("lastName"))
            outStr2 += ','
            outStr2 += str(dictx.get("firstName"))
            outStr2 += ','
            outStr2 += str(dictx.get("title"))
            outStr2 += ','
            outStr2 += str(dictx.get("location"))
            outStr2 += '\n'

    print(outStr, cnt)
    print(outStr2)

listManagers(myEmloyeeList)

# calc percentage of contractores
outStr = "Total contractors:"
cnt = 0
prcnt = 0
for dictx in myEmloyeeList:
    if dictx.get("title") == "Contractor":
        cnt += 1
print(outStr, cnt, f'{pct(cnt, len(myEmloyeeList)):.2f}%','\n')

# update one recored after a promotion
outStr = "Updated one record after promotion: "
cnt = 0
for dictx in myEmloyeeList:
    if dictx.get("lastName") == "Siddaq" and dictx.get("firstName") == "Hasan":
        dictx.update({"management": True})
        cnt += 1
print(outStr, cnt)

listManagers(myEmloyeeList)

print("All Done")