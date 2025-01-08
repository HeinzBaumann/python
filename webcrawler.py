import requests
from bs4 import BeautifulSoup

# Fetch the web page
url = "https://www.demorgen.be"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract all <script> tags
scripts = soup.find_all('script')

# Search for API references
api_call_count = 0
for script in scripts:
    script_content = script.get('src') or script.string
    if script_content and '__tcfapi' in script_content:
        api_call_count += 1
        print("API reference found: {script_content}")
    #if script_content:
    #    print("API reference found: ")
    #    print(script_content)

print(f"Total embedded API references: {api_call_count}")
print("Total embedded API references \"__tcfapi(\'addEventListener\', 2, func())\"")
