#!/usr/bin/python3
import requests
from bs4 import *
import random

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/{}.0'.format(random.randint(1,20))}
r = requests.get("https://www.whatismyip.com",headers=headers)
if not r.ok:
    print(r.text)
    quit()
s = BeautifulSoup(r.text,'html.parser')
print(s.find('li',attrs={'class':'list-group-item'}).text.lstrip())
