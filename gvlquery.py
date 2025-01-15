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
gvlf = urlopen(strGvl).read()
dictGvl = json.loads(gvlf)
dictVendors = dictGvl['vendors']

# Print the current date and time
print("Date queries for GVL...")
print("Date and time:", datetime.datetime.now())

# return the header infor and total number of vendors in the GVL
print("gvlSpecificationVersion: ", dictGvl['gvlSpecificationVersion'])
print("vendorListVersion",  dictGvl['vendorListVersion'])
print("Total numbers of vendors: ", len(dictVendors))

cnt = 0
for x in dictVendors:
    if len(dictVendors[x]['purposes']) == 0 and len(dictVendors[x]['legIntPurposes']) == 0 and len(dictVendors[x]['specialPurposes']) > 0:
     cnt += 1
     # print("id: " + x +  " name: " + dictVendors[x]['name'])
print("Total with special purposes only: ", cnt)

# The number of Vendors that have declared at least one purpose based on LI + at least one SP 
# (those will still have ambiguity in their signalling after the update)

cnt = 0
for x in dictVendors:
    if len(dictVendors[x]['purposes']) == 0 and len(dictVendors[x]['legIntPurposes']) > 0 and len(dictVendors[x]['specialPurposes']) > 0:
     cnt += 1
     # print("id: " + x +  " name: " + dictVendors[x]['name'])
print("Total with LI and special purposes: ", cnt)

# the number of Vendors that have declared only purposes based on consent (no LI) + at least one SP 
# (those will have the signalling ambiguity removed with the upcoming update to the library)

cnt = 0
for x in dictVendors:
    if len(dictVendors[x]['purposes']) > 0 and len(dictVendors[x]['legIntPurposes']) == 0 and len(dictVendors[x]['specialPurposes']) > 0:
     cnt += 1
     # print("id: " + x +  " name: " + dictVendors[x]['name'])
print("Total with only purposes consent and special purposes: ", cnt)

print("Done with GVL data.")

#
# query somethings from the AVI JSON file
#

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

unclassifiedList = []
dictCountry = { "GERMANY" : 0 }
cnt = 0
for x in dictAviVendors:
    addrStr = dictAviVendors[x]['legalAddress']
    addrList = addrStr.rsplit(';')
    i = len(addrList)
    cStr = addrList[i - 1]
    cStr = cStr.upper()
    cStr = cStr.rstrip(" ")  # remove trailing spaces
    # check for spelling error and know variations and fix these
    if cStr == "UNITED KINDOM" or cStr == "UNITED KINGDON" or cStr == "UNITED KINGOM" or cStr == "ENGLAND" or cStr == "GREAT BRITAIN" or cStr == "LONDON":
        cStr = "UNITED KINGDOM"
    elif cStr == "USA" or cStr == "UNITED STATE" or cStr == "THE USA" or cStr == "UNITED STATES OF AMERICA":
        cStr = "UNITED STATES"
    elif cStr == "THE NETHERLANDS" or cStr == "NEDERLAND":
        cStr = "NETHERLANDS"
    elif cStr == "TURKIYE" or cStr == "TÜRKIYE":
        cStr = "TURKEY"
    elif cStr == "VEINNA" or cStr == "VIENA" or cStr == "VIENNA":
        cStr = "AUSTRIA"
    elif cStr == "DANMARK":
        cStr = "DENMARK"
    elif cStr == "DÜSSELDORF" or cStr == "MÜNCHEN" or cStr == "NÜRNBERG" or cStr == "GERMANDY" or cStr == "HAMBORG":
        cStr = "GERMANY"
    elif cStr == "ITALIA":
        cStr = "ITALY"
    elif cStr == "SLOVENIJA":
        cStr = "SLOVENIA"
    elif cStr == "SCHWEIZ":
        cStr = "SWITZERLAND"
    elif cStr == "ESPAÑA":
        cStr = "SPAIN"
    elif cStr == "BRAZIL":
        cStr = "BRASIL"
    elif cStr == "PARIS":
        cStr = "FRANCE"
    elif re.search("[0-9]", cStr):
        unclassifiedList.append(cStr)
        cStr = "Z_UNCLASSIFIED"      
            
    myList = list(dictCountry.keys())
    try:
        y = myList.index(cStr)
        cnt = dictCountry.get(cStr)
        cnt += 1
        dictCountry.update({cStr: cnt})
    except ValueError:
        # add the new string to the dictionary
        dictCountry.update({cStr: 1})

## output the country listing:
print("List of Countries:")
sorted_dict = dict(sorted(dictCountry.items(), key=lambda item: item[0]))
cCnt = 0
for x in sorted_dict:
  print(f"{x:<24} {sorted_dict[x]}")
  cCnt += sorted_dict[x]
str = "Total entries found:"
print(f"{str:<24} {cCnt}")
## output the unclassified list:
outStr = ""
for x in unclassifiedList:
    outStr += x
    outStr += ', '
print("Z_UNCLASSIFIED:", outStr.rstrip(", "))

# operating environments
cntWeb = 0
cntMobile = 0
cntCTV = 0

for x in dictAviVendors:
    for y in dictAviVendors[x]['environments']:
        if y == 'Web':
            cntWeb += 1
        if y == 'Native App (Mobile)':
            cntMobile += 1
        if y == 'Native App (CTV)':
            cntCTV += 1

str = "Vendor operating on Web:"
print(f"{str:<28} {cntWeb}")
str = "Vendor operating on Mobile:"
print(f"{str:<28} {cntMobile}")
str = "Vendor operating on CTV:"
print(f"{str:<28} {cntCTV}")
print("Done with AVI data.")