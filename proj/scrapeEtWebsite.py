import requests
import asyncio
import json
import os
from bs4 import BeautifulSoup
from celery import Celery
from celery.schedules import crontab
import socketio


app = Celery('proj',
             broker='amqp://guest:guest@localhost:5672/celery',
             backend='rpc://guest:guest@localhost:5672/celery',)

app.conf.timezone = 'Asia/Kolkata'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/newCleanScreenerData.json') as f:
        data = json.load(f)
        for stock in data:
            sender.add_periodic_task(crontab(minute="*/3", day_of_week="mon-fri"), etWebScrape.s(
                data[stock].get('seoName'), data[stock].get('companyId'), stock), name=f"fetching {stock}")


@app.task
def etWebScrape(companySeoName, companyId, scrip):
    with requests.Session() as s:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        content = s.get(
            f"https://economictimes.indiatimes.com/{companySeoName}/stocks/companyid-{companyId}.cms", headers=headers)
        stockPage = BeautifulSoup(content.text, "html.parser")
        extractedLtp = stockPage.find("span", {"class": "ltp"})
        extractedChange = stockPage.find("span", {"class": "absoluteChange"})
        ltp = float("".join(extractedLtp.string.split(",")))
        change = float("".join(extractedChange.string.split(",")))
        changePercent = round((ltp / (ltp - change) - 1) * 100, 2)
        req_body = {scrip: {"scrip": scrip, "ltp": ltp,
                            "change": change, "changePercent": changePercent}}
        sio = socketio.Client()
        sio.connect('http://localhost:7000', transports=['websocket'])
        sio.emit('stock-server', data=req_body)
        print(req_body)
