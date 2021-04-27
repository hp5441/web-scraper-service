import requests
import json
from dotenv import load_dotenv

CSRF_TOKEN = os.getenv("CERF_TOKEN")

with requests.Session() as s:
    headers = {"Content-Type": "application/json",
               "X-CSRFToken": CSRF_TOKEN,
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}

    with open("newCleanScreenerData.json") as f:
        data = json.load(f)
        for i in data:
            temp_body = {}
            temp_body['scrip'] = i
            temp_body['name'] = data[i].get('companyName')
            temp_body['ltp'] = data[i].get('ltp')
            temp_body['change'] = data[i].get('absoluteChange')
            temp_body['marketcap'] = data[i].get('marketCapValue')
            temp_body['sector'] = data[i].get('sectorName')
            temp_body['pe_ratio'] = data[i].get('pe')
            temp_body['industry_pe'] = data[i].get('industryPe')
            temp_body['pb_ratio'] = data[i].get('pb')
            temp_body['de_ratio'] = data[i].get('debtEquityRatio')
            temp_body['eps'] = data[i].get('eps')
            temp_body['promoter_holding'] = data[i].get('promotorHolding')
            temp_body['fii_holding'] = data[i].get('fiiHolding')
            temp_body['dii_holding'] = data[i].get('diiHolding')
            temp_body['f_promoter_holding'] = data[i].get('foreignPromotor')
            resp = s.post(
                f"http://localhost:8000/api/stock/stocksdetail/{i}/", json=temp_body, headers=headers)
