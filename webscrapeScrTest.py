import json
import requests

jsonbody = {
    "pageNumber": 1,
    "sortedField": "marketCapValue",
    "pageSize": "1673",
    "sortedOrder": "desc",
    "exchangeId": "50",
    "customFilterDtoList": [],
    "isBankingSector": "false",
    "fieldNames": "*"
}

headers = {"Content-Type": "application/json",
           "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}

with requests.Session() as s:
    temp_json = s.post(
        "https://etmarketsapis.indiatimes.com/ET_Screeners/getFilteredData", json=jsonbody, headers=headers).json()
    with open("screenerData.json", "w") as file:
        json.dump(temp_json, file, indent=4)
