import requests
import datetime
import json

formattedDate = "".join(datetime.date.today().isoformat().split('-'))

with requests.Session() as s:
    headers = {
        'origin':'https://www.bseindia.com',
        'referer':'https://www.bseindia.com/',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    content = s.get(f"https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w?strCat=-1&strPrevDate={formattedDate}&strScrip=&strSearch=P&strToDate={formattedDate}&strType=C", headers=headers)
    print(json.loads(content.text))