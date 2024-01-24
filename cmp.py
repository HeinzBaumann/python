import json
import urllib
from urllib.request import urlopen

strCmp = "https://cmp-list.consensu.org/v2/cmp-list.json"
f = urlopen(strCmp).read()
dictCmp = json.loads(f)
dictVendors = dictCmp['cmps']
#return the total number of vendors in the Cmp
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

for x in dictVendors:
  if 'deletedDate' in dictVendors[x]:
    print(dictVendors[x]['name'])

#return the number of operatable vendors
i = 0
for x in dictVendors:
  if 'deletedDate' not in dictVendors[x]:
    i += 1
print("Number of operatable vendors: ", i)

