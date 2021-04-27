import json
import os

temp = {}

with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/newCleanScreenerData.json') as f:
    data = json.load(f)
    for stock in data:
        temp[stock] = {
            'task': 'proj.scrapeEtWebsite.etWebScrape',
            # , day_of_week='mon-fri'),
            'schedule': 'crontab(hour=[9, 10, 11, 12, 13, 14, 15])',
            'args': (data[stock].get('seoName'), data[stock].get('companyId'), stock)
        }
    with open("jsonToBeatConf.json", "w") as o:
        json.dump(temp, o, indent=4)
