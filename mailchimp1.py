#
# routine to match up mailchimp records with records from zulu5
# output list with email addressed to be imported into mailchimp as an tagged audience
#
# June 2026 - Heinz Baumann
#
# TODO: improve the search / comparison
# TODO: check for if no TAGS are set for a company found
# TODO: fix skipped items

import csv
import urllib
from urllib.request import urlopen

vendorListMailChimpStr = "subscribed_email_audience_export_0618.csv"
#vendorListGivenStr = "vendor_table.csv"
vendorListGivenStr = "mismatches.csv"
outputFileStr = "mailchimpFile.csv"
#outputCsvStr = "Company,Email Address,TAGS\n"
outputCsvStr = "Email Address\n"
outputList = []
skipListStr = ""
emailfilterList = ["tech", "support", "privacy", "sysadmin", "compliance", "billing", "admin", "legal"]

def checkTag(listInput):
   targets = ["Technical", "Legal"]
   return any(item in listInput for item in targets)

print("Processing...")
with open(vendorListGivenStr, mode='r', newline='', encoding='utf-8') as file:
    # Automatically uses the first row as dictionary keys
    dict1 = csv.DictReader(file)
    cnt = 0
    cnt1 = 0
    cnf = 0
    tStr = ""
    notFoundList = []
    skipList = []
    skipped = 0
    for row in dict1:
        # Access values directly using the column names
        cnt += 1
        with open(vendorListMailChimpStr, mode='r', newline='', encoding='utf-8') as file2:
          dict2 = csv.DictReader(file2)
          fnd = False
          skip = False
          
          for row2 in dict2:
            if ((row['Vendor Name'].casefold() in row2['Company'].casefold()) and (checkTag(row2['TAGS']) or (len(row2['TAGS']) == 0))):
                # cleanCompanyName = row2['Company'].casefold().replace(",", "")
                # tStr = cleanCompanyName + "," + row2['Email Address'] + "\n"
                tmpStr = row2['Email Address'].split('@')[0]
                if tmpStr.casefold() in emailfilterList:
                    if skip == False or fnd == False:
                        skipList.append(row2['Email Address'])
                        skip = True
                        skipped += 1
                        fnd = True
                else:
                    tStr = row2['Email Address'] + "\n"
                    outputList.append(tStr)
                    if fnd == False:
                      fnd = True
                      cnt1 += 1
        
        if (fnd == False):
          notFoundList.append(row['Vendor Name'].casefold())

    # Check for partial matches
    notFoundList2 = []
    if (len(notFoundList) > 0): 
      for item in notFoundList:
          fnd = False
          skip = False
          with open(vendorListMailChimpStr, mode='r', newline='', encoding='utf-8') as file2:
            dict2 = csv.DictReader(file2)
            for row2 in dict2:
                tStr = row2['Company'].casefold()
                if len(tStr) > 1:
                  tstr2 = tStr.rsplit(' ', 1)[0]
                  if (tstr2 in item) and (checkTag(row2['TAGS']) or (len(row2['TAGS']) == 0)):
                    #cleanStr = row2['Company'].casefold().replace(",", "")
                    #tStr = cleanStr + "," + row2['Email Address'] + "\n"
                    tStr = row2['Email Address'] + "\n"
                    tmpStr = tStr.split('@')[0]
                    if tmpStr.casefold() in emailfilterList:
                      if skip == False or fnd == False:
                        skipped += 1
                        skip = True
                        fnd = True
                    else:
                      outputList.append(tStr)
                      if fnd == False:
                        cnt1 += 1
                        fnd = True
          if fnd == False:
            notFoundList2.append(item)
        
    # Search the remaining not found items by matching its first word. Remaining will be printed as errors
    notFoundList3 = []
    if (len(notFoundList2)): 
      for item in notFoundList2:
          itemSplit = item.split()[0]
          fnd = False
          with open(vendorListMailChimpStr, mode='r', newline='', encoding='utf-8') as file2:
            dict2 = csv.DictReader(file2)
            for row2 in dict2:
                tStr = row2['Company'].casefold()
                if len(tStr) > 1:
                  if itemSplit in tStr:
                    if checkTag(row2['TAGS']) or (len(row2['TAGS']) == 0):
                      tStr = row2['Email Address'] + "\n"
                      tmpStr = tStr.split('@')[0]
                      if tmpStr.casefold() in emailfilterList:
                        if skip == False or fnd == False:
                          skipped += 1
                          skip = True
                          fnd == True
                      else:
                        outputList.append(tStr)
                        if fnd == False:
                          cnt1 += 1
                          fnd = True
          if fnd == False:
            notFoundList3.append(item)

# generate the output string that we write out
outputList.sort()
clean_list = list(dict.fromkeys(outputList))
tStr = "".join(clean_list)
outputCsvStr += tStr
# output the outputCsvStr to a file
print("Writing output file: ", outputFileStr)
with open(outputFileStr, "w", encoding="utf-8") as file:
    file.write(outputCsvStr)

# sort and remove dups from notFoundList
notFoundList3.sort()
notFoundCleanList = list(dict.fromkeys(notFoundList3))
# sort the and remove dups from the skipList
skipList.sort()
skipListClean = list(dict.fromkeys(skipList))

# return the total number of vendors in the list
print("Total number of entries found: ", cnt)
print("Total number of entries processed: ", cnt1)
print("Total skipped items: ", len(skipListClean))
print("Error: Items not able to match: ", len(notFoundList3), "\n\tItems: ", notFoundCleanList)
print("Warning: Group aliases ", emailfilterList," skipped: ", len(skipListClean), "\n\tItems: ", skipListClean)
