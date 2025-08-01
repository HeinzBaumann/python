#
# gvlquery.py
# 
# query the GVL for any thing we are interested in 
# query the AVI for any thing we are interested in
#
# argument -v  verbose output 
#
# Todo: 
#
# implement the verbose option
#
import json
import urllib
from urllib.request import urlopen
import datetime
import re

strGvl = "https://vendor-list.consensu.org/v3/vendor-list.json"
strAvi = "https://vendor-list.consensu.org/v2/additional-vendor-information-list.json"
# strGvl = "https://vendor-list.consensu.org/v2/archives/vendor-list-v51.json" # use to test the tcfapi tests
# strGvl = "https://vendor-list.consensu.org/v3/archives/vendor-list-v86.json" # end of 2024
gvlf = urlopen(strGvl).read()
dictGvl = json.loads(gvlf)
dictVendors = dictGvl['vendors']

# Print the current date and time
print("Date queries for GVL...")
print("Date and time:", datetime.datetime.now())

# return the header info and total number of vendors in the GVL
print("File used:", strGvl.rsplit('/', 1)[1])
print("gvlSpecificationVersion:", dictGvl['gvlSpecificationVersion'])
print("vendorListVersion:",  dictGvl['vendorListVersion'])
print("lastUpdated:", dictGvl['lastUpdated'])
print("Total numbers of vendors:", len(dictVendors))

# 
# returns the number of vendors per purpose
# 

def find_element(arr, target):
    try:
        return arr.index(target)
    except ValueError:
        return -1

def checkForElementsWo234(element1, element2):
    if find_element(element1, 2) == -1 \
        and find_element(element1, 3) == -1 \
        and find_element(element1, 4) == -1 \
        and find_element(element2, 2) == -1 \
        and find_element(element2, 3) == -1 \
        and find_element(element2, 4) == -1:
        return 1
    else:
        return 0

# vendor list storage
outputVendorList = []
outputVendorsDeclaringConsent = []
outputVendorsDeclaringLI = []
printOutput = []

# - Total number of Vendors that declare purpose 7
cnt = 0
cntLi = 0

for x in dictVendors:
    if 'deletedDate' not in dictVendors[x] and len(dictVendors[x]['purposes']) != 0 \
        and find_element(dictVendors[x]['purposes'], 7) != -1:
        cnt += 1

for x in dictVendors:
    if 'deletedDate' not in dictVendors[x] and len(dictVendors[x]['legIntPurposes']) != 0 \
        and find_element(dictVendors[x]['legIntPurposes'], 7) != -1:
        cntLi += 1

print("***Vendors that have declared Purpose 7: " + str(cnt+cntLi) + " (LI purpose 7: " + str(cntLi) + ")")

# + total number of Vendors that declare purpose 7 but none of the purposes 2,3,4
cnt = 0
cntLi = 0
outputVendorList.append("\nVendors that have declared Purpose 7 but none of the purposes 2,3,4:")
outputVendorsDeclaringConsent.append("\nVendors that have declared Purpose 7 but none of the purposes 2,3,4 (consent):")
outputVendorsDeclaringLI.append("\nVendors that have declared Purpose 7 but none of the purposes 2,3,4 (Legitimate Interest):")

for x in dictVendors:
    if 'deletedDate' not in dictVendors[x]:
        if len(dictVendors[x]['purposes']) != 0 and len(dictVendors[x]['legIntPurposes']) != 0:
            if find_element(dictVendors[x]['purposes'], 7) != -1 \
            and checkForElementsWo234(dictVendors[x]['purposes'], dictVendors[x]['legIntPurposes']) == 1:
                outputVendorList.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                outputVendorsDeclaringConsent.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                cnt += 1
            elif find_element(dictVendors[x]['legIntPurposes'], 7) != -1 \
            and checkForElementsWo234(dictVendors[x]['purposes'], dictVendors[x]['legIntPurposes']) == 1:
                outputVendorList.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                outputVendorsDeclaringLI.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                cnt += 1
        elif len(dictVendors[x]['purposes']) != 0:
            if find_element(dictVendors[x]['purposes'], 7) != -1 \
            and checkForElementsWo234(dictVendors[x]['purposes'], dictVendors[x]['legIntPurposes']) == 1:
                outputVendorList.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                outputVendorsDeclaringConsent.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                cnt += 1
        elif len(dictVendors[x]['legIntPurposes']) != 0:
            if find_element(dictVendors[x]['legIntPurposes'], 7) != -1 \
            and checkForElementsWo234(dictVendors[x]['purposes'], dictVendors[x]['legIntPurposes']) == 1:
                outputVendorList.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                outputVendorsDeclaringLI.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                cnt += 1

# Format the vendor output list
printOutput.extend(outputVendorList)
printOutput.extend(outputVendorsDeclaringConsent)
printOutput.extend(outputVendorsDeclaringLI)
outputVendorList = []
outputVendorsDeclaringConsent = []
outputVendorsDeclaringLI = []

for x in dictVendors:
    if 'deletedDate' not in dictVendors[x] and len(dictVendors[x]['legIntPurposes']) != 0 \
        and find_element(dictVendors[x]['legIntPurposes'], 7) != -1 \
        and find_element(dictVendors[x]['purposes'], 2) == -1 \
        and find_element(dictVendors[x]['purposes'], 3) == -1 \
        and find_element(dictVendors[x]['purposes'], 4) == -1 \
        and find_element(dictVendors[x]['legIntPurposes'], 2) == -1 \
        and find_element(dictVendors[x]['legIntPurposes'], 3) == -1 \
        and find_element(dictVendors[x]['legIntPurposes'], 4) == -1:
        cntLi += 1

print("***Vendors that have declared Purpose 7 but none of the purposes 2,3,4: " + str(cnt) + " (LI Purposes: " + str(cntLi) +")") 

# total number of Vendors that declare purpose 8
cnt = 0
cntLi = 0
for x in dictVendors:
    if 'deletedDate' not in dictVendors[x] and len(dictVendors[x]['purposes']) != 0 \
        and find_element(dictVendors[x]['purposes'], 8) != -1:
        cnt += 1

for x in dictVendors:
    if 'deletedDate' not in dictVendors[x] and len(dictVendors[x]['legIntPurposes']) != 0 \
        and find_element(dictVendors[x]['legIntPurposes'], 8) != -1:
        cntLi += 1

print("***Vendors that have declared Purpose 8: " + str(cnt+cntLi) + " (LI purpose 8: " + str(cntLi) + ")")

# total number of Vendors that declare purpose 8 but none of the purposes 2,3,4
cnt = 0
cntLi = 0
outputVendorList.append("\nVendors that have declared Purpose 8 but none of the purposes 2,3,4:")
outputVendorsDeclaringConsent.append("\nVendors that have declared Purpose 8 but none of the purposes 2,3,4 (consent):")
outputVendorsDeclaringLI.append("\nVendors that have declared Purpose 8 but none of the purposes 2,3,4 (Legitimate Interest):")

for x in dictVendors:
    if 'deletedDate' not in dictVendors[x]:
        if len(dictVendors[x]['purposes']) != 0 and len(dictVendors[x]['legIntPurposes']) != 0:
            if find_element(dictVendors[x]['purposes'], 8) != -1 \
            and checkForElementsWo234(dictVendors[x]['purposes'], dictVendors[x]['legIntPurposes']) == 1:
                outputVendorList.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                outputVendorsDeclaringConsent.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                cnt += 1
            elif find_element(dictVendors[x]['legIntPurposes'], 8) != -1 \
            and checkForElementsWo234(dictVendors[x]['purposes'], dictVendors[x]['legIntPurposes']) == 1:
                outputVendorList.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                outputVendorsDeclaringLI.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                cnt += 1
        elif len(dictVendors[x]['purposes']) != 0:
            if find_element(dictVendors[x]['purposes'], 8) != -1 \
            and checkForElementsWo234(dictVendors[x]['purposes'], dictVendors[x]['legIntPurposes']) == 1:
                outputVendorList.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                outputVendorsDeclaringConsent.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                cnt += 1
        elif len(dictVendors[x]['legIntPurposes']) != 0:
            if find_element(dictVendors[x]['legIntPurposes'], 8) != -1 \
            and checkForElementsWo234(dictVendors[x]['purposes'], dictVendors[x]['legIntPurposes']) == 1:
                outputVendorList.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                outputVendorsDeclaringLI.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                cnt += 1

# Format the vendor output list
printOutput.extend(outputVendorList)
printOutput.extend(outputVendorsDeclaringConsent)
printOutput.extend(outputVendorsDeclaringLI)
outputVendorList = []
outputVendorsDeclaringConsent = []
outputVendorsDeclaringLI = []

for x in dictVendors:
    if 'deletedDate' not in dictVendors[x] and len(dictVendors[x]['legIntPurposes']) != 0 \
        and find_element(dictVendors[x]['legIntPurposes'], 8) != -1 \
        and find_element(dictVendors[x]['purposes'], 2) == -1 \
        and find_element(dictVendors[x]['purposes'], 3) == -1 \
        and find_element(dictVendors[x]['purposes'], 4) == -1 \
        and find_element(dictVendors[x]['legIntPurposes'], 2) == -1 \
        and find_element(dictVendors[x]['legIntPurposes'], 3) == -1 \
        and find_element(dictVendors[x]['legIntPurposes'], 4) == -1:
        cntLi += 1

print("***Vendors that have declared Purpose 8 but none of the purposes 2,3,4: " + str(cnt) + " (LI Purposes: " + str(cntLi) +")") 

# Total number of Vendors that declare purpose 9
cnt = 0
cntLi = 0
for x in dictVendors:
    if 'deletedDate' not in dictVendors[x] and len(dictVendors[x]['purposes']) != 0 \
        and find_element(dictVendors[x]['purposes'], 9) != -1:
        cnt += 1

for x in dictVendors:
    if 'deletedDate' not in dictVendors[x] and len(dictVendors[x]['legIntPurposes']) != 0 \
        and find_element(dictVendors[x]['legIntPurposes'], 9) != -1:
        cntLi += 1

print("***Vendors that have declared Purpose 9: " + str(cnt+cntLi) + " (LI purpose 9: " + str(cntLi) + ")")

# total number of Vendors that declare purpose 9 but none of the purposes 2,3,4
cnt = 0
cntLi = 0
outputVendorList.append("\nVendors that have declared Purpose 9 but none of the purposes 2,3,4:")
outputVendorsDeclaringConsent.append("\nVendors that have declared Purpose 9 but none of the purposes 2,3,4 (consent):")
outputVendorsDeclaringLI.append("\nVendors that have declared Purpose 9 but none of the purposes 2,3,4 (Legitimate Interest):")

for x in dictVendors:
    if 'deletedDate' not in dictVendors[x]:
        if len(dictVendors[x]['purposes']) != 0 and len(dictVendors[x]['legIntPurposes']) != 0:
            if find_element(dictVendors[x]['purposes'], 9) != -1 \
            and checkForElementsWo234(dictVendors[x]['purposes'], dictVendors[x]['legIntPurposes']) == 1:
                outputVendorList.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                outputVendorsDeclaringConsent.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                cnt += 1
            elif find_element(dictVendors[x]['legIntPurposes'], 9) != -1 \
            and checkForElementsWo234(dictVendors[x]['purposes'], dictVendors[x]['legIntPurposes']) == 1:
                outputVendorList.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                outputVendorsDeclaringLI.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                cnt += 1
        elif len(dictVendors[x]['purposes']) != 0:
            if find_element(dictVendors[x]['purposes'], 9) != -1 \
            and checkForElementsWo234(dictVendors[x]['purposes'], dictVendors[x]['legIntPurposes']) == 1:
                outputVendorList.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                outputVendorsDeclaringConsent.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                cnt += 1
        elif len(dictVendors[x]['legIntPurposes']) != 0:
            if find_element(dictVendors[x]['legIntPurposes'], 9) != -1 \
            and checkForElementsWo234(dictVendors[x]['purposes'], dictVendors[x]['legIntPurposes']) == 1:
                outputVendorList.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                outputVendorsDeclaringLI.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                cnt += 1

for x in dictVendors:
    if 'deletedDate' not in dictVendors[x] and len(dictVendors[x]['legIntPurposes']) != 0 \
        and find_element(dictVendors[x]['legIntPurposes'], 9) != -1 \
        and find_element(dictVendors[x]['purposes'], 2) == -1 \
        and find_element(dictVendors[x]['purposes'], 3) == -1 \
        and find_element(dictVendors[x]['purposes'], 4) == -1 \
        and find_element(dictVendors[x]['legIntPurposes'], 2) == -1 \
        and find_element(dictVendors[x]['legIntPurposes'], 3) == -1 \
        and find_element(dictVendors[x]['legIntPurposes'], 4) == -1:
        cntLi += 1

# Format the vendor output list
printOutput.extend(outputVendorList)
printOutput.extend(outputVendorsDeclaringConsent)
printOutput.extend(outputVendorsDeclaringLI)
outputVendorList = []
outputVendorsDeclaringConsent = []
outputVendorsDeclaringLI = []

print("***Vendors that have declared Purpose 9 but none of the purposes 2,3,4: " + str(cnt) + " (LI Purposes: " + str(cntLi) +")")

# Total number of Vendors that declare at least one of these three purposes (7, 8 or 9)
cnt = 0
for x in dictVendors:
    if 'deletedDate' not in dictVendors[x] and len(dictVendors[x]['purposes']) != 0 \
        and (find_element(dictVendors[x]['purposes'], 7) != -1 \
        or find_element(dictVendors[x]['purposes'], 8) != -1 \
        or find_element(dictVendors[x]['purposes'], 9) != -1 \
        or find_element(dictVendors[x]['legIntPurposes'], 7) == -1 \
        and find_element(dictVendors[x]['legIntPurposes'], 8) == -1 \
        and find_element(dictVendors[x]['legIntPurposes'], 8) == -1):
        cnt += 1

print("***Vendors that declare at least one of these three purposes 7, 8 or 9: " + str(cnt))

# total number of Vendors that declare at least one of these three purposes (7, 8 or 9) but none of the purposes 2,3,4
cnt = 0
cntLI = 0
outputVendorList.append("\nVendors that declare at least one of these three purposes (7, 8 or 9) but none of the purposes 2,3,4:")
outputVendorsDeclaringConsent.append("\nVendors that declare at least one of these three purposes (7, 8 or 9) but none of the purposes 2,3,4 (consent):")
outputVendorsDeclaringLI.append("\nVendors that declare at least one of these three purposes (7, 8 or 9) but none of the purposes 2,3,4 (Legitimate Interest):")

for x in dictVendors:
    if 'deletedDate' not in dictVendors[x]:
        if len(dictVendors[x]['purposes']) != 0 and len(dictVendors[x]['legIntPurposes']) != 0:
            if (find_element(dictVendors[x]['purposes'], 7) != -1 \
                or find_element(dictVendors[x]['purposes'], 8) != -1 \
                or find_element(dictVendors[x]['purposes'], 9) != -1 ) \
                and checkForElementsWo234(dictVendors[x]['purposes'], dictVendors[x]['legIntPurposes']) == 1:
                outputVendorList.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                outputVendorsDeclaringConsent.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                cnt += 1
            elif (find_element(dictVendors[x]['legIntPurposes'], 7) != -1 \
                or find_element(dictVendors[x]['legIntPurposes'], 8) != -1 \
                or find_element(dictVendors[x]['legIntPurposes'], 9) != -1 ) \
                and checkForElementsWo234(dictVendors[x]['purposes'], dictVendors[x]['legIntPurposes']) == 1:
                outputVendorList.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                outputVendorsDeclaringLI.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                cnt += 1
        elif len(dictVendors[x]['purposes']) != 0:
            if (find_element(dictVendors[x]['purposes'], 7) != -1 \
                or find_element(dictVendors[x]['purposes'], 8) != -1 \
                or find_element(dictVendors[x]['purposes'], 9) != -1 ) \
                and checkForElementsWo234(dictVendors[x]['purposes'], dictVendors[x]['legIntPurposes']) == 1:
                outputVendorList.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                outputVendorsDeclaringConsent.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                cnt += 1
        elif len(dictVendors[x]['legIntPurposes']) != 0:
            if (find_element(dictVendors[x]['legIntPurposes'], 7) != -1 \
                or find_element(dictVendors[x]['legIntPurposes'], 8) != -1 \
                or find_element(dictVendors[x]['legIntPurposes'], 9) != -1 ) \
                and checkForElementsWo234(dictVendors[x]['purposes'], dictVendors[x]['legIntPurposes']) == 1:
                outputVendorList.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                outputVendorsDeclaringLI.append(str(dictVendors[x]['id']) + " " + dictVendors[x]['name'])
                cnt += 1

# Format the vendor output list
printOutput.extend(outputVendorList)
printOutput.extend(outputVendorsDeclaringConsent)
printOutput.extend(outputVendorsDeclaringLI)
outputVendorList = []
outputVendorsDeclaringConsent = []
outputVendorsDeclaringLI = []

for x in dictVendors:
    if 'deletedDate' not in dictVendors[x] and len(dictVendors[x]['legIntPurposes']) != 0 \
        and (find_element(dictVendors[x]['legIntPurposes'], 7) != -1 \
            or find_element(dictVendors[x]['legIntPurposes'], 8) != -1 \
            or find_element(dictVendors[x]['legIntPurposes'], 9) != -1 ) \
        and find_element(dictVendors[x]['purposes'], 2) == -1 \
        and find_element(dictVendors[x]['purposes'], 3) == -1 \
        and find_element(dictVendors[x]['purposes'], 4) == -1 \
        and find_element(dictVendors[x]['legIntPurposes'], 2) == -1 \
        and find_element(dictVendors[x]['legIntPurposes'], 3) == -1 \
        and find_element(dictVendors[x]['legIntPurposes'], 4) == -1:
        cntLi += 1

print("***Vendors that declare at least one of these three purposes (7, 8 or 9) but none of the purposes 2,3,4: " + str(cnt) + " (LI Purposes: " + str(cntLi) +")")

# Total number of Vendors that declared themselves as "Website analytics" and/or "Campaign analytics" and/or "Audience analytics" (based on the additional vendor information list here)
avif = urlopen(strAvi).read()
dictAvi = json.loads(avif)
dictAviVendors = dictAvi['vendors']

print("\n")
print("Date queries for AVI...")
print("Date and time:", datetime.datetime.now())

# return the header info and total number of vendors in the AVI
str = "aviSpecificationVersion:"
print(f"{str:<28} {dictAvi['aviSpecificationVersion']}")
str = "aviSpecificationVersion:"
print(f"{str:<28} {dictAvi['aviSpecificationVersion']}")
str = "aviListVersion:"
print(f"{str:<28} {dictAvi['aviListVersion']}")
str = "Total numbers of vendors:"
print(f"{str:<28} {len(dictAviVendors)}")

cnt = 0
for x in dictAviVendors:
    if find_element(dictAviVendors[x]['serviceTypes'], "Website Analytics") != -1 \
        or find_element(dictAviVendors[x]['serviceTypes'], "Audience Analytics") != -1 \
        or find_element(dictAviVendors[x]['serviceTypes'], "Campaign Analytics") != -1: 
        cnt += 1
print("Total number of vendors delared Website, Campaign and/or Audience Analytics: ", cnt)

# Total number of Vendors that declared themselves as "Website analytics" and/or "Campaign analytics" and/or "Audience analytics" and nothing else
cnt = 0
tempServiceTypes = {}
for x in dictAviVendors:
    if len(dictAviVendors[x]['serviceTypes']) > 0 and len(dictAviVendors[x]['serviceTypes']) < 4:
        tempServiceTypes[x] = dictAviVendors[x]['serviceTypes']
        cnt += 1

#print("\n")
#for x in tempServiceTypes:
#    print(tempServiceTypes[x])

cnt = 0
for x in tempServiceTypes:
    isClean = True
    for strElement in tempServiceTypes[x]:
        if strElement != "Website Analytics" \
           and strElement != "Audience Analytics" \
           and strElement != "Campaign Analytics":
            isClean = False;
    if isClean == True:
        # print(tempServiceTypes[x])
        cnt += 1

print("Total number of vendors delared Website, Campaign and/or Audience Analytics and nothing else: ", cnt)

print("\nFinished with data mining.")
print("\nDump vendor names...")
for x in printOutput:
    print(x)
print("\nJob done")