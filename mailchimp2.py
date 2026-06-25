#
# routine to handle bounce email lists from MailChimp  
# it concatinates the lists together and dedups them for further processing
# Input file name bounce1.csv - bounce3.csv
# Output: BounceList.csv
# The format of the Bouncelist.csv is a CSV file with one columne Email Address
#
# June 2026 - Heinz Baumann
#
# TODO: Add bounce type

import csv

bounceFileList = [ "bounce1.csv", "bounce2.csv", "bounce3.csv" ]
outputBounceListFile = "bounceList.csv"

bouncedList = []
outputCsvStr = "Email Addresses\n"

print("Processing...")

for inputFileStr in bounceFileList:
  with open(inputFileStr, mode='r', newline='', encoding='utf-8') as file:
    # Automatically uses the first row as dictionary keys
    dict1 = csv.DictReader(file)
    for row in dict1:
        bouncedList.append(row['email'])

# generate the output string that we write out
bouncedList.sort()
cleantBouncedList = list(dict.fromkeys(bouncedList))
tStr = "\n".join(cleantBouncedList)
outputCsvStr += tStr
# output the outputCsvStr to a file
print("Writing output file: ", outputBounceListFile)
with open(outputBounceListFile, "w", encoding="utf-8") as file:
    file.write(outputCsvStr)

# return the total number of vendors in the list
print("Total number of bounced email addressed: ", len(cleantBouncedList))