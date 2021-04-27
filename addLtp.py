import json

output = {}

with open("cleanScreenerData.json") as f:
    data = json.load(f)
    with open("screenerData.json") as m:
        olddata = json.load(m).get("page")
        for stock in olddata:
            print(stock)
            temp_dict = {}
            temp_dict['companyName'] = stock.get('companyName')
            temp_dict['ltp'] = stock.get('ltp')
            temp_dict['absoluteChange'] = data[stock.get(
                'symbol')].get('absoluteChange')
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
            output[stock.get('symbol')] = temp_dict

with open("newCleanScreenerData.json", "w") as o:
    json.dump(output, o, indent=4)
