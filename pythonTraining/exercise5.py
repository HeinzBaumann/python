# exercise 5
# Lists, Dictionaries
# Json object
# Accessing files
# stats on GVL / Additional Vendor Data 
# Datetime functions
#
# query the GVL
# query the AVI
# query the CMP
#

# imports
import json
from urllib.request import urlopen
import datetime
import re

# GVL list
strGvl = "https://vendor-list.consensu.org/v3/vendor-list.json"

# open file into memory
gvlf = urlopen(strGvl).read()
# load the JSON file and initialize our GLV dictionary
dictGvl = json.loads(gvlf)
# initialize our vendors dictionary
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

# take a look at the JSON element for a vendor
# print("Debug: JSON Element TCF vendor: ")
# print(dictVendors['1'])
# print()
#
# {
# 'id': 1, 'name': 'Exponential Interactive, Inc d/b/a VDX.tv', 
# 'purposes': [1, 2, 3, 4, 7, 8, 9, 10], 'legIntPurposes': [], 
# 'flexiblePurposes': [2, 7, 8, 9, 10], 'specialPurposes': [1, 2], 
# 'features': [1, 2, 3], 'specialFeatures': [], 
# 'cookieMaxAgeSeconds': 7776000, 
# 'usesCookies': True, 'cookieRefresh': True, 
# 'urls': [{'langId': 'en', 'privacy': 'https://vdx.tv/privacy/', 
# 'legIntClaim': 'https://www.exponential.com/wp-content/uploads/2018/04/Balancing-Assessment-for-Legitimate-Interest-Publishers-v2.pdf'}], 
# 'usesNonCookieAccess': False, 
# 'dataRetention': {'stdRetention': 397, 'purposes': {}, 'specialPurposes': {}}, 
# 'dataDeclaration': [1, 3, 4, 6, 8, 10, 11],
# 'deviceStorageDisclosureUrl': 'https://tribalfusion.com/compliance_devicestorage_hosting.json'
# }
#

# Exercise 1: how many operational vendors do we have?
cnt = 0
for x in dictVendors:
    if 'deletedDate' in dictVendors[x]:
        cnt += 1
print("Total operational vendors:", len(dictVendors) - cnt)

# Exercise 2: print the total of vendors using perpose 11
def findElementInList(list, value):
    for x in list:
       if x == value:
          return True
    return False

cnt = 0
for x in dictVendors:
    if len(dictVendors[x]['purposes']) > 0 and findElementInList(dictVendors[x]['purposes'], 11):
        cnt += 1

print("Total vendors who declared purpose 11: ", cnt)

# Exercise 3: how many vendors have a date retention of 365 days or more?
# Extra: print the vendors with a data retention bigger than 365 days

# {'stdRetention': 397, 'purposes': {}, 'specialPurposes': {}}
iRetention = 365
outStr = "Vendors who declare a retention period over " + str(iRetention) + " days:\n"

def dataRetentionGreaterThenGivenDays(dict, value):
    if len(dict):
        if dict.get('stdRetention') != None and dict['stdRetention'] > value:
            return True
        for x in dict['purposes']:
            if dict.get('purposes') != None and dict['purposes'][x] > value:
                return True
        # return True if we find a specialPurpose retention bigger than value


        return False
    
for x in dictVendors:
    if dataRetentionGreaterThenGivenDays(dictVendors[x]['dataRetention'], iRetention):
       cnt += 1
       outStr = outStr + str(dictVendors[x]['id']) + ' ' + dictVendors[x]['name'] + '\n'

print(outStr)
print("Total vendors that have a data retention of", str(iRetention), "days or larger:", cnt)

# exercise: stats from the AVI JSON file
strAvi = "https://vendor-list.consensu.org/v2/additional-vendor-information-list.json"
avif = urlopen(strAvi).read()
dictAvi = json.loads(avif)
dictAvis = dictAvi['vendors']
# print(dictAvis['1'])

# {
# 'id': 1, 'name': 'Exponential Interactive, Inc d/b/a VDX.tv', 
# 'legalAddress': 'Exponential Interactive Spain S.L.;General Martinez Campos Num 41;Madrid;28010;Spain', 
# 'contact': 'tim.sleath@vdx.tv', 'territorialScope': ['FR', 'DE', 'NL', 'ES', 'GB'], 
# 'environments': ['Web', 'Native App (CTV)'], 'serviceTypes': ['SSP', 'DSP', 'Ad Serving'], 
# 'internationalTransfers': True, 'transferMechanisms': ['SCCs']
# }

# exercise: vendors who transfer data outside Europe
# extra: under which contract

outStr = "Vendors who transfer data outside Europe:\nVendor\tTransfer Mechanism"
cnt = 0
for x in dictAvis:
    if dictAvis[x]['internationalTransfers'] and dictAvis[x]['internationalTransfers'] == True:
        # count the number of vendors transfering data outside EU
        # create a output string with the list of vendors and their transfer mechanism
        
        
        outStr += '\n'
print(outStr)
print('Total number of vendors who transfer data outside Europe:', cnt)

# exercise: stats from the CMP JSON file
# CMP list
strCmp = "https://cmp-list.consensu.org/v2/cmp-list.json"
cmpf = urlopen(strCmp).read()
dictCmp = json.loads(cmpf)
dictCmps = dictCmp['cmps']

# print a CMP record
# print(dictCmps['2'])

# {
# 'id': 2, 'name': 'AppConsent by SFBX® ', 'isCommercial': True, 
# 'environments': ['Web', 'Native App (Mobile)', 'Native App (CTV)']
# }

# exercise: total number of vendor and list of vendors supporting Natice App (Mobile)
outStr = "\nList of CMPs supporting Native App (Mobile): \n"
cnt = 0

for x in dictCmps:
    if dictCmps[x].get('environments') and dictCmps[x]['environments']:
        for y in dictCmps[x]['environments']:
            if (y == 'Native App (Mobile)'):
                cnt += 1
                outStr += dictCmps[x]['name']
                outStr += '\n'
print(outStr)
print("Total CMPs supporting  Native App (Mobile): ", cnt)

print("\nAll jobs done!")