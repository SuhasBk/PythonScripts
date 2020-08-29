#!/usr/local/bin/python3
import requests
from bs4 import BeautifulSoup

r = requests.get("http://wikipedia.com/wiki/Special:Random", headers={'User-Agent':'masterbyte'})

p = BeautifulSoup(r.text,'html.parser').select('p')

for i in p:
    if i.text!='':
        print(i.text)
