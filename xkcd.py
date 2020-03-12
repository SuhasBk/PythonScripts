#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from subprocess import run,PIPE

r = requests.get("https://c.xkcd.com/random/comic/",headers={'User-Agent':'Not A Bot!'})
data = BeautifulSoup(r.text,'html.parser').select('img')[2].get('src')
img_url = 'http:'+data
print(img_url)
run(["mpv",img_url,"--loop=inf"],stdout=PIPE,stderr=PIPE)
