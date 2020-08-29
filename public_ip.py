#!/usr/local/bin/python3
import requests
from bs4 import BeautifulSoup
import random

headers = {'User-Agent': 'masterbyte'}
r = requests.get("https://www.whatismyip.com",headers=headers)
if not r.ok:
    print(r.text)
    quit()
s = BeautifulSoup(r.text,'html.parser')
print(s.find('li',attrs={'class':'list-group-item'}).text.lstrip())
