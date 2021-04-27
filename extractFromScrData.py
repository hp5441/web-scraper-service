import json
output = {}
with open("screenerData.json") as f:
    data = json.load(f)
    for stock in data.get('page'):
        temp_dict = {}
        temp_dict['companyName'] = stock.get('companyName')
        temp_dict['ltp'] = stock.get('ltp')
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
    with open("cleanScreenerData.json", "w") as o:
        json.dump(output, o, indent=4)
