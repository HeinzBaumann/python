#
# crawls the given webpage (argv[1]) for __tcfapi('addEventHandler' calls and
# returns the number of calls found as well as it prints the actual call line
# to see the URLs that it crawls you can remove the comment at the statement 
# print(f"Crawling: {url}") online 22
#

import requests
from bs4 import BeautifulSoup
import re
import sys

visited_urls = set()
api_counter = 0
cnt = 0

def crawl_page(url, base_url):
    global api_counter
    global cnt
    cnt += 1

    if url in visited_urls or not url.startswith(base_url):
        return  # Avoid re-visiting or leaving the domain
    
    visited_urls.add(url)
    print(f"Crawling: {url}")

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        # Analyze <script> tags
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and "addEventListener" in script.string:
                # print(f"API call found in inline script on {url}")
                if 'tcfapi("addEventListener"' in script.string or 'tcfapi(\'addEventListener\'' in script.string:
                    api_counter += 1

            if script.get('src'):
                external_script_url = script['src']
                if external_script_url.startswith('/'):
                    external_script_url = base_url + external_script_url
                analyze_external_script(external_script_url)

        # Recursively crawl links
        links = soup.find_all('a', href=True)
        # print(links)
        # i = 0
        # for item in links:
        #     i += 1
        # print(i)
        for link in links:
            crawl_page(link['href'], base_url)
            if cnt > 512000:
                break

    except requests.exceptions.RequestException as e:
        print(f"Error crawling {url}: {e}")

def analyze_external_script(script_url):
    global api_counter
    try:
        response = requests.get(script_url)
        # print(response.text)
        # if '__tcfapi(\'addEventListener\',' in response.text:
        if 'tcfapi("addEventListener"' in response.text or 'tcfapi(\'addEventListener\'' in response.text:
            # Extract the API call
            start = response.text.find("__tcfapi")
            end = start + 64
            if start != -1:
                substring = response.text[start:end]
                print(substring)
                api_counter += 1
    except requests.exceptions.RequestException as e:
        print(f"Error fetching script {script_url}: {e}")

# Start crawling
start_url = ""
if len(sys.argv) > 1:
    start_url = sys.argv[1]

if start_url:
    crawl_page(start_url, start_url)
    print(f"Total scanned urls: {cnt}")
    print(f"Total embedded API \"__tcfapi(\'addEventListener\',...\") references: {api_counter}")
else:
    print ("Error: Missing webpage URL argument.")
