#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from subprocess import run,PIPE
from fake_useragent import UserAgent

r = requests.get("https://c.xkcd.com/random/comic/",headers={'User-Agent':UserAgent().random})
data = BeautifulSoup(r.text,'html.parser').select('img')[2].get('src')
img_url = 'http:'+data
print(img_url)
run(["vlc",img_url],stdout=PIPE,stderr=PIPE)
