import requests
import csv
import sys

def fetchPrices(filename):
    url = 'https://archives.nseindia.com/content/equities/EQUITY_L.csv'
    temparray=[]
    with requests.Session() as s:
        content = s.get(url=url)
        decodedContent = content.content.decode('utf-8')
        reader = csv.reader(decodedContent.splitlines(), delimiter=',')
        for row in list(reader):
            temparray.append(row[0])
    with open(filename, 'w') as f:
        f.write('stocks = [')
        for i in range(1, len(temparray)):
            if i==len(temparray)-1:
                f.write('"'+str(temparray[i])+'"')
            else:
                f.write('"'+str(temparray[i])+'"'+', ')
        f.write(']')

if __name__ == "__main__":
    fetchPrices(sys.argv[1])