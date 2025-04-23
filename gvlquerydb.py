from __future__ import print_function

import requests
import argparse
import json
import re
from collections import Counter

from apiclient import discovery
from google.oauth2 import service_account

import datetime
    
def main():
    """Extract data from the global vendor list Google sheet and convert to the vendor list JSON format
    """
     # Print thetitle and current date and time
    print("Querying the TCF vendor Database\t", datetime.datetime.now())
    
    # BEARER TOKEN for VRMP Endpoint
    BEARER_FILE = './auth/bearer_token.json'
    # REST API-Endpoint
    url = "https://ziqra6nd5p.eu-central-1.awsapprunner.com/api/export/vendor-eu" 
    
    def read_bearer_token(file_path):
        try:
            with open(file_path, 'r') as file:
                bearer_token = file.read().strip()  # Strip to remove any newline characters
        except FileNotFoundError:
            print(f"Error: {file_path} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        return(bearer_token)
    
    bearer_token = read_bearer_token(BEARER_FILE)
    # print(bearer_token)

    
    # HTTP-Header with Bearer-Token
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }

    # Send Reqeust for VRMP REST-Endpoint 
    response = requests.get(url, headers=headers)

    # Check if request was successfully
    if response.status_code == 200:
        json_object = response.json()
        # Extract vendor output from json content
        helper = json_object["vendors"]
        queryData(helper)
    else:
        print(f"Error consuming endpoint: {response.status_code} - {response.text}")

# 
# returns the number of vendors per purpose
# 

def find_element(arr, target):
    try:
        return arr.index(target)
    except ValueError:
        return -1

def queryData(dictVendors):
    # return total number of vendors in the database
    print("Total numbers of vendors:\t", len(dictVendors))
    cntDeleted = 0
    for x in dictVendors:
        if 'deletedDate' in dictVendors[x]:
            cntDeleted += 1
    print("Total number of opertational vendors:\t" , len(dictVendors) - cntDeleted)
    print("Total deleted vendors:\t", cntDeleted)
    
    cnt = 0
    for x in dictVendors:
        if 'deletedDate' not in dictVendors[x] and len(dictVendors[x]['purposes']) == 0 and len(dictVendors[x]['legIntPurposes']) == 0 and len(dictVendors[x]['specialPurposes']) > 0:
         cnt += 1
    print("Total with special purposes only:\t", cnt)

    print("***Number of vendors per purpose:\t")
    def num_vendors_per_purpose(purpose_no):
        cnt = 0
        for x in dictVendors:
            if 'deletedDate' not in dictVendors[x] and len(dictVendors[x]['purposes']) != 0 and find_element(dictVendors[x]['purposes'], purpose_no) != -1:
                cnt += 1
        print("Vendors with purpose " + str(purpose_no) + ":\t" + str(cnt))

    for x in range(1, 12):
        num_vendors_per_purpose(x)

    #print("***Done with number of purposes by vendor")

    #
    # returns the number of vendors not using purpse 2,3,4 and 7
    #

    cnt = 0
    for x in dictVendors:
        if 'deletedDate' not in dictVendors[x] and len(dictVendors[x]['purposes']) != 0 \
            and find_element(dictVendors[x]['purposes'], 2) == -1 \
            and find_element(dictVendors[x]['purposes'], 3) == -1 \
            and find_element(dictVendors[x]['purposes'], 4) == -1 \
            and find_element(dictVendors[x]['purposes'], 7) == -1:
            cnt += 1
    for x in dictVendors:
        if 'deletedDate' not in dictVendors[x] and len(dictVendors[x]['purposes']) == 0:
            cnt += 1

    print("Vendors that have not declared either Purpose 2,3,4 and 7:\t" + str(cnt))

    print("Done with GVL data.")

if __name__ == '__main__':
    main()
