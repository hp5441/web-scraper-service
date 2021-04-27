import requests
import json
from bs4 import BeautifulSoup

output = {}

with requests.Session() as s:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    with open("screenerData.json") as f:
        data = json.load(f)
        for stock in data.get('page'):
            content = s.get(
                f"https://economictimes.indiatimes.com/{stock.get('seoName')}/stocks/companyid-{stock.get('companyId')}.cms", headers=headers)
            soup = BeautifulSoup(content.text, 'html.parser')
            temp = soup.find('span', {'class': 'absoluteChange'})
            temp_dict = {}
            temp_dict['companyName'] = stock.get('companyName')
            temp_dict['seoName'] = stock.get('seoName')
            temp_dict['marketCapValue'] = stock.get('marketCapValue')
            temp_dict['companyId'] = stock.get('companyId')
            temp_dict['sectorName'] = stock.get('sectorName')
            temp_dict['pe'] = stock.get('pe')
            temp_dict['industryPe'] = stock.get('industryPe')
            temp_dict['pb'] = stock.get('pb')
            temp_dict['debtEquityRatio'] = stock.get('debtEquityRatio')
            temp_dict['eps'] = stock.get('eps')
            temp_dict['promotorHolding'] = stock.get('promotorHolding')
            temp_dict['fiiHolding'] = stock.get('fiiHolding')
            temp_dict['diiHolding'] = stock.get('diiHolding')
            temp_dict['foreignPromotor'] = stock.get('forignPromotor')
            if temp:
                print(temp.string, stock.get('symbol'))
                temp_dict['absoluteChange'] = temp.string
            else:
                temp_dict['absoluteChange'] = 0
            output[stock.get('symbol')] = temp_dict
    with open("cleanScreenerData.json", "w") as o:
        json.dump(output, o, indent=4)
