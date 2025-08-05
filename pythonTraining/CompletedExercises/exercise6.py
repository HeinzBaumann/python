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

# AVI JSON file
strAvi = "https://vendor-list.consensu.org/v2/additional-vendor-information-list.json"
avif = urlopen(strAvi).read()
dictAvi = json.loads(avif)
dictAvis = dictAvi['vendors']

# Print the current date and time
print("Date queries for GVL...")
print("Date and time:", datetime.datetime.now())

# return the header info and total number of vendors in the GVL
print("File used:", strGvl.rsplit('/', 1)[1], 'and', strAvi.rsplit('/', 1)[1])
print("gvlSpecificationVersion:", dictGvl['gvlSpecificationVersion'])
print("vendorListVersion:",  dictGvl['vendorListVersion'])
print("lastUpdated:", dictGvl['lastUpdated'])

#print("Total numbers of vendors:", len(dictVendors))

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
# {
# 'id': 1, 'name': 'Exponential Interactive, Inc d/b/a VDX.tv', 
# 'legalAddress': 'Exponential Interactive Spain S.L.;General Martinez Campos Num 41;Madrid;28010;Spain', 
# 'contact': 'tim.sleath@vdx.tv', 'territorialScope': ['FR', 'DE', 'NL', 'ES', 'GB'], 
# 'environments': ['Web', 'Native App (CTV)'], 'serviceTypes': ['SSP', 'DSP', 'Ad Serving'], 
# 'internationalTransfers': True, 'transferMechanisms': ['SCCs']
# }

# Output a combined list GVL and AVI
cnt = 0

outStr = "Id, Name, dataRetention, cookieMaxAge, Territoral Scope, Environment\n"

deletedVendors = []
for x in dictVendors:
    if 'deletedDate' in dictVendors[x]:
        deletedVendors.append(dictVendors[x]['id']) 

for x in dictVendors:
    if 'deletedDate' in dictVendors[x]:
        continue
    outStr = outStr + str(dictVendors[x]['id']) + ',' + dictVendors[x]['name'] + ',' + str(dictVendors[x]['dataRetention']) + ',' + str(dictVendors[x]['cookieMaxAgeSeconds']) + ','
    if dictAvis[x]['id'] in deletedVendors:
        continue
    else:
        outStr = outStr + str(dictAvis[x]['territorialScope']) + ',' + str(dictAvis[x]['environments'])
    outStr += '\n'
    
print(outStr)