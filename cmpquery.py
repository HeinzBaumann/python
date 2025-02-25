#
# cmpquery.py
# 
# query the CMP for any thing we are interested in 
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

strCmp = "https://cmp-list.consensu.org/v2/cmp-list.json"
# strCmp = "https://cmp-list.consensu.org/v2/archives/cmp-list.2024-12-26.json" # end of 2024
cmpf = urlopen(strCmp).read()
dictCmp = json.loads(cmpf)
dictCmps = dictCmp['cmps']

# Print the current date and time
print("Date queries for CMP...")
print("Date and time:", datetime.datetime.now())

# return the header info and total number of CMPs in the CMP List
print("File used:", strCmp.rsplit('/', 1)[1])
print("lastUpdated",  dictCmp['lastUpdated'])
print("Total numbers of CMPs: ", len(dictCmps))

cnt = 0

# operating environments
cntWeb = 0
cntMobile = 0
cntCTV = 0
cntWebMobile = 0
cntWebCtv = 0
cntWebMobileCtv = 0
cntMobileCtv = 0
cntCtvOnly = 0
cntWebOnly = 0
cntMobileOnly = 0

x1 = 0
x2 = 0
x3 = 0

for x in dictCmps:
    if ('environments' in dictCmps[x]):
        for y in dictCmps[x]['environments']:
            if y == 'Web':
                cntWeb += 1
                x1 = x
            if y == 'Native App (Mobile)':
                cntMobile += 1
                if x1 == x:
                    cntWebMobile += 1
                x2 = x
            if y == 'Native App (CTV)':
                cntCTV += 1
                if x1 == x and x2 == 0:
                    cntWebCtv += 1
                if x1 == x and x2 == x:
                    cntWebMobileCtv += 1
                if x1 != x and x2 == x:
                    cntMobileCtv += 1
                if x1 != x and x2 != x:
                    cntCtvOnly += 1
                x3 = x
        if x3 == 0 and x2 == 0:
            cntWebOnly += 1
        if x1 == 0 and x3 == 0:
            cntMobileOnly += 1
        x2 = 0
        x3 = 0
        x1 = 0

str = "CMP operating on Web:"
print(f"{str:<28} {cntWeb}")
str = "CMP operating on Mobile:"
print(f"{str:<28} {cntMobile}")
str = "CMP operating on CTV:"
print(f"{str:<28} {cntCTV}")
str = "CMP operating on Web and Mobile:"
print(f"{str:<28} {cntWebMobile}")
str = "CMP operating on Web and CTV:"
print(f"{str:<28} {cntWebCtv}")
str = "CMP operating on Mobile and CTV:"
print(f"{str:<28} {cntMobileCtv}")
str = "CMP operating on Web, Mobile and CTV:"
print(f"{str:<28} {cntWebMobileCtv}")
str = "CMP operating on Web only:"
print(f"{str:<28} {cntWebOnly}")
str = "CMP operating on Mobile only:"
print(f"{str:<28} {cntMobileOnly}")
str = "CMP operating on CTV only:"
print(f"{str:<28} {cntCtvOnly}")
print("Done with CMP data.")