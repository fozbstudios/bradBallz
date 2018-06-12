import requests
import os

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://crunchtimebaseball.com/baseball_map.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}

response = requests.get('http://crunchtimebaseball.com/master.csv', headers=headers)
# Throw an error for bad status codes
response.raise_for_status()

with open('temp.csv', 'wb') as handle:
    for block in response.iter_content(1024):
        handle.write(block)
with open("temp.csv", "r",encoding='iso-8859-1') as inp, open("namesToCheckAgainst.csv", "w",encoding='iso-8859-1') as out:
    lines = inp.readlines()
    skip =True
    # for li in lines:
    for i in range(0,10):
        li = lines[i]
        if skip:
            skip=False
            continue
        else:
            sp = li.split(',')
            stw=sp[0]+','+sp[1]+'\n'
            out.write(stw)
os.remove("temp.csv")
os.rename('namesToCheckAgainst.csv','bradBallz/namesToCheckAgainst.csv')
