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
    # Extract data from the CMP information from the database

    # Print title and the current date and time
    print("Data query for CMPs\t", datetime.datetime.now())

    #BEARER TOKEN for VRMP Endpoint
    BEARER_FILE = './auth/bearer_token.json'
    # REST API-Endpoint
    url = "https://ziqra6nd5p.eu-central-1.awsapprunner.com/api/export/cmp-eu" 
    
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
        #Extract vendor output from json content
        helper = json_object["cmps"]
        printHeaderInfo(json_object)
        queryData(helper)
    else:
        print(f"Error consuming endpoint: {response.status_code} - {response.text}")

def printHeaderInfo(dictCmp):
    print("CMP data last modified:\t", dictCmp["lastModified"])

def find_element(arr, target):
    try:
        return arr.index(target)
    except ValueError:
        return -1

def queryData(dictCmps):
    # return total number of CMPs in the CMP List
    print("Total numbers of CMPs:\t", len(dictCmps))

    cnt = 0
    for x in dictCmps:
        if 'deletedDate' in dictCmps[x]:
            cnt += 1
    print("Total operational CMPs:\t", len(dictCmps) - cnt)
    print("Total deleted CMPs:\t", cnt)

    cnt = 0

   # return operating environment data
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
        if ('environments' in dictCmps[x]) and 'deletedDate' not in dictCmps[x]:
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
    # print(f"{str:<28} {cntWeb}")
    print(str,"\t", cntWeb)
    str = "CMP operating on Mobile:"
    print(str,"\t", cntMobile)
    str = "CMP operating on CTV:"
    print(str,"\t", cntCTV)
    str = "CMP operating on Web and Mobile:"
    print(str,"\t", cntWebMobile)
    str = "CMP operating on Web and CTV:"
    print(str,"\t", cntWebCtv)
    str = "CMP operating on Mobile and CTV:"
    print(str,"\t", cntMobileCtv)
    str = "CMP operating on Web, Mobile and CTV:"
    print(str,"\t", cntWebMobileCtv)
    str = "CMP operating on Web only:"
    print(str,"\t", cntWebOnly)
    str = "CMP operating on Mobile only:"
    print(str,"\t", cntMobileOnly)
    str = "CMP operating on CTV only:"
    print(str,"\t", cntCtvOnly)

    print("Done with CMP data.")

if __name__ == '__main__':
    main()
