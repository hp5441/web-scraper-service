from time import perf_counter, sleep
import requests
import json
import aiohttp
import asyncio
import sys
import websocket
from .celery import app


class async_client():

    def __init__(self):
        self.session = None
        self.count = 0

    def getUrl(self, scrip):
        return f"https://json.bselivefeeds.indiatimes.com/ET_Community/currenttick?scripcode={scrip}EQ&exchangeid=50&directions=current&callback=serviceHit.autoLoadResultCallback&scripcodetype=company"

    async def fetch(self, scrip):
        if not self.session:
            self.session = aiohttp.ClientSession()
            await self.session.get(self.getUrl(scrip))
        else:
            async with self.session.get(self.getUrl(scrip)) as response:

                json_data = await response.text()
                json_data = json_data.strip()[34:-1]
                pydict = json.loads(json_data)
                parametervalues = pydict['query']['parametervalues']
                stockdata = pydict['query']['results']['quote'][0]
                stockstatus = pydict['query']['marketstatus']['currentMarketStatus']
                self.count += 1
                return parametervalues['scripcode'], stockdata['Close'], stockstatus, stockdata['DateTemp'], self.count, stockdata
        print(self.session)


def getNseUrl(scrip):
    return f"https://www.nseindia.com/api/quote-equity?symbol={scrip}"


async def main(client, scrips):
    tasks = [asyncio.create_task(client.fetch(scrip)) for scrip in scrips]
    results = await asyncio.gather(*tasks)
    return results


async def run_test(client, company):
    try:
        return await main(client, company)
    except Exception as e:
        print('loop done')


async def run_test_counter(count, client, company):
    results = await asyncio.gather(*(run_test(client, company) for _ in range(count)))
    return results


async def run_test_counter_periodic(total, interval, count, client, company, final):
    await client.fetch('MBLINFRA')
    while total > 0:
        start = perf_counter()
        results = await run_test_counter(count, client, company)
        print(results)
        print(perf_counter() - start)
        sleep(interval)
        total -= 1
    final[0] = results
    await client.session.close()


async def closeClientSession(client):
    await client.session.close()


@app.task
def scrape(*companies):
    client = async_client()
    scrapedResults = [0]
    asyncio.run(run_test_counter_periodic(
        1, 0, 1, client, companies, scrapedResults))
    #socket = websocket.WebSocket()
    # socket.connect("ws://localhost:8000/ws/stock/")
    # socket.send(json.dumps({
    #    'message': {'name': 'RELIANCE', 'data': scrapedResults[0]}
    # }))
    return scrapedResults[0]
