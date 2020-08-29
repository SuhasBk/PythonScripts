#!/usr/local/bin/python3
import requests
import os,sys,webbrowser
from bs4 import BeautifulSoup
from subprocess import run,PIPE

r = requests.get("https://c.xkcd.com/random/comic/", headers={'User-Agent': 'masterbyte'})
data = BeautifulSoup(r.text,'html.parser').select('img')[2].get('src')
img_url = 'http:'+data
print(img_url)

if sys.platform.startswith("linux"):
    os.system("xdg-open "+img_url)
elif sys.platform == "darwin":
    os.system("open "+img_url)
else:
    webbrowser.open(img_url)
