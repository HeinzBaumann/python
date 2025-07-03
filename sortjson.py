import json
from datetime import datetime

strJsonFile = "datafiles\\translationslist.json"
f = open(strJsonFile , "r")
dictCmp = json.load(f)
dictTranslations = dictCmp['languages']
# print(dictTranslations)

# return the total number of translations in the Cmp
l1 = len(dictTranslations)
print(f"Total numbers of translations: {l1}")

# print the sorted lanaguage list
sorted_by_langId_asc = sorted(dictTranslations, key=lambda x: x['langStr'], reverse=False)
# print(json.dumps(sorted_by_langId_asc, indent=4))

# now output the new sorted JSON file
filename = "datafiles\\newtranslationlist.json"
f2 = open(filename, 'w', encoding='utf-8')
lastUpdateDate = datetime.utcnow()
formatedDateTime = lastUpdateDate.strftime("%Y-%m-%dT%H:%M:%SZ")
# print(formatedDateTime)
# increment the version when an update happens
version = 2
jsonHeader = f"""{{
   \"languageListFormat\": 1,
   \"languageListVersion\": {version},
   \"lastUpdated\": \"{formatedDateTime}\",
   \"languages\": ["""
jsonDataWithLanguages = jsonHeader + json.dumps(sorted_by_langId_asc)
newJsonData = jsonDataWithLanguages + """
]
}"""
outJson = json.loads(newJsonData)
#print(json.dumps(outJson, indent=4))

json.dump(outJson, f2, indent=4, ensure_ascii=False)
print(f"JSON data successfully written to {filename}")