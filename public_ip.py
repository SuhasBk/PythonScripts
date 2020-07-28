#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import random
from fake_useragent import UserAgent

headers = {'User-Agent':UserAgent().random}
r = requests.get("https://www.whatismyip.com",headers=headers)
if not r.ok:
    print(r.text)
    quit()
s = BeautifulSoup(r.text,'html.parser')
print(s.find('li',attrs={'class':'list-group-item'}).text.lstrip())
