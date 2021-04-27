import requests
import re
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

CSRF_TOKEN = os.getenv("CSRF_TOKEN")

with requests.Session() as s:
    with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/newCleanScreenerData.json') as f:
        data = json.load(f)
        headers = {"Content-Type": "application/json",
                   "X-CSRFToken": CSRF_TOKEN,
                   "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        for stock in data:
            content = s.get(
                f"https://economictimes.indiatimes.com/{data[stock].get('seoName')}/stocks/{data[stock].get('seoName')}/stocksupdate/companyid-{data[stock].get('companyId')}.cms")
            stockNews = BeautifulSoup(content.text, "html.parser")
            stockNewsUpdates = stockNews.find_all("div", "eachStory")
            for i in stockNewsUpdates:
                temp_body = {}
                if str(i.span.string).strip()[2:] == "Announcement" and i.a:
                    temp_body['stock'] = stock
                    temp_body['date'] = datetime.strptime(
                        " ".join(re.split(',\s|,|\s', i.time.string)[:-1]), "%d %b %Y %I:%M%p").isoformat()
                    temp_body['news-title'] = i.h3.string
                    temp_body['news-item'] = i.p.string
                    temp_body['news-type'] = i.span.string.strip()[2:]
                    temp_body['attachment'] = i.a.get('href') if i.a else None
                    """print(i.h3.string, "|"+i.span.string.strip()
                          [2:]+"|", datetime.strptime(" ".join(re.split(',\s|,|\s', i.time.string)[:-1]), "%d %b %Y %I:%M%p"), i.a.get('href'))"""
                else:
                    temp_body['stock'] = stock
                    temp_body['date'] = datetime.strptime(
                        " ".join(re.split(',\s|,|\s', i.time.string)[:-1]), "%d %b %Y %I:%M%p").isoformat()
                    temp_body['news-title'] = i.h3.string
                    temp_body['news-item'] = i.p.string
                    temp_body['news-type'] = i.span.string.strip()[2:]
                    temp_body['link'] = "https://economictimes.indiatimes.com" + \
                        i.h3.a.get("href") if i.h3.a else None
                    """print(i.h3.string, "|"+i.span.string.strip()
                          [2:]+"|", i.time.string+" |","https://economictimes.indiatimes.com"+i.h3.a.get("href") if i.h3.a else None)"""

                s.post(
                    f"http://localhost:8000/api/stock/stocknews/", json=temp_body, headers=headers)
