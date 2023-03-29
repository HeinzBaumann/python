import json
import urllib
from urllib.request import urlopen

strGvl = "https://vendor-list.consensu.org/v2/vendor-list.json"
f = urlopen(strGvl).read()
dictGvl = json.loads(f)
dictVendors = dictGvl['vendors']
#return the total number of vendors in the GVL
print("Total numbers of vendors: ")
print(len(dictVendors))

## return the vendor list
## print("Vendor list dump: ")
## print(dictVendors)

##return the names of the vendors
##print("Vendor names: ")
##for x in dictVendors:
###  print(x)
#  print(dictVendors[x]['name'])
###  print(dictVendors[x])

#return the numbers and names of deleted vendor
i = 0
for x in dictVendors:
  if 'deletedDate' in dictVendors[x]:
    i += 1
print("Number of deleted vendors: ", i)

## print the names of the deleted vendors:

##
## TODO
##

#return the number of operatable vendors
i = 0
for x in dictVendors:
  if 'deletedDate' not in dictVendors[x]:
    i += 1
print("Number of operatable vendors: ", i)

