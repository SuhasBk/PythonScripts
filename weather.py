#!/usr/local/bin/python3
import requests, sys
from bs4 import BeautifulSoup

try:
    country = sys.argv[1]
    city = sys.argv[2]
except:
    exit('usage: python weather.py [country] [city]')

headers = {'User-Agent': 'masterbyte'}
r = requests.get(f"https://www.timeanddate.com/weather/{country}/{city}",headers=headers)
if r.ok:
    s = BeautifulSoup(r.text,'html.parser')
    a = s.find('div',attrs={'id':'qlook'})
    res = ''
    try:
        for i in list(a)[1::]:
            if i.text.count('°C') > 1:
                for j in i.text.split('°C'):
                    res+=j+'\n'
            else:
                res+=i.text+'\n'
        print(res.replace('\n', '. '))
    except:
        print("Bad city")
else:
    exit(f"Request error : {r.status_code}")
