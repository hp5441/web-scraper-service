from time import perf_counter, sleep
import requests
import json
import aiohttp
import asyncio
import sys
import websocket
import os

headers = {"Content-Type": "application/json",
           "X-CSRFToken": "kkgthZHIFyWLvJ3xOQcxMVy5xIGxRX6VOmV3vXZxF5Mm5BAbUojGOJCMygaoAnej",
           "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}


class async_client():

    def __init__(self):
        self.session = None
        self.count = 0

    def getUrl(self, scrip):
        return f"https://etelection.indiatimes.com/ET_Charts/GetCompanyPriceInformation?scripcode={scrip}EQ&exchangeid=50&datatype=eod&filtertype=eod&tagId=30660&directions=back&scripcodetype=company&uptodataid=&period=1w"

    async def fetch(self, scrip):
        if not self.session:
            self.session = aiohttp.ClientSession()
            await self.session.get(self.getUrl(scrip))
        else:
            async with self.session.get(self.getUrl(scrip)) as response:

                json_data = await response.text()
                return json_data
        print(self.session)

    async def postToApi(self, scrip, data):
        if not self.session:
            self.session = aiohttp.ClientSession()
            await self.session.get(self.getUrl(scrip))
        else:
            data['stock'] = scrip
            await self.session.post(f"http://localhost:8000/api/stock/stockprice/{scrip}/", headers={"Content-Type": "application/json",
                                                                                                     "X-CSRFToken": "kkgthZHIFyWLvJ3xOQcxMVy5xIGxRX6VOmV3vXZxF5Mm5BAbUojGOJCMygaoAnej",
                                                                                                     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}, json=data)


def getNseUrl(scrip):
    return f"https://www.nseindia.com/api/quote-equity?symbol={scrip}"


"""async def main(client, scrips):
    tasks = [asyncio.create_task(client.fetch(scrip)) for scrip in scrips]
    results = await asyncio.gather(*tasks)
    return results"""


"""async def run_test(client, company):
    try:
        return await main(client, company)
    except Exception as e:
        print('loop done')"""


async def run_test(client, stock):
    await client.fetch('MBLINFRA')
    start = perf_counter()

    with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/newCleanScreenerData.json') as f:
        data = json.load(f)
        tempFlag = False
        for stock in data:
            # if stock=="VESUVIUS":
            #     tempFlag=True
            # if tempFlag: 
            results = await client.fetch(stock if '&' not in stock else "%26".join(stock.split('&')))
            data_points = json.loads(results)['query']['results']['quote']
            for i in range(1):
                if data_points and data_points[i].get("Date", None)=="2021-04-26":
                    tasks = [asyncio.create_task(client.postToApi(
                        stock, datap)) for datap in data_points[:i+1]]
                    post_results = await asyncio.gather(*tasks)
                    sleep(1)
                    print(post_results)
    await client.session.close()

if __name__ == "__main__":
    client = async_client()
    asyncio.run(run_test(client, "MBLINFRA"))

"""with requests.Session() as s:
    data = s.get("https://etelection.indiatimes.com/ET_Charts/GetCompanyPriceInformation?scripcode=MBLINFRAEQ&exchangeid=50&datatype=eod&filtertype=eod&tagId=30660&firstreceivedataid=2021-4-1&lastreceivedataid=&directions=back&scripcodetype=company&uptodataid=&period=5y", headers=headers)
    print(data.json()['query']['results']['quote'])"""
