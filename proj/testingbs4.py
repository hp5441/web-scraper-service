import requests
from bs4 import BeautifulSoup

with requests.Session() as s:
    content = s.get("https://economictimes.indiatimes.com/mbl-infrastructures-ltd/stocks/companyid-30660.cms")
    soup = BeautifulSoup(content.text, 'html.parser')
    para_temp = soup.find("p", "para").find_all("span", "para")
    for i in para_temp:
        print(i.string.extract())
