#!/usr/local/bin/python3
import requests
import sys
import webbrowser
import os
import shutil
from bs4 import BeautifulSoup

headers = {'User-Agent': 'masterbyte'}

session = requests.Session()

if len(sys.argv[1:]) > 0:
    search_term = ' '.join(sys.argv[1:])
else:
    search_term = input("Enter the search term:\n> ")

try:
    os.mkdir(search_term.replace(" ","_"))
except OSError:
    pass

def view(path):
    if sys.platform.startswith("linux"):
        os.system("xdg-open "+path)
    elif sys.platform == "darwin":
        os.system("open "+path)
    else:
        webbrowser.open(path)

r = session.get(f"https://api.flickr.com/services/feeds/photos_public.gne?tags={search_term}",headers=headers)

s = BeautifulSoup(r.text,'lxml')
links = s.findAll("link",{"rel":"enclosure","type":"image/jpeg"})

try:
    for link in links[:5]:
        fname = os.path.join(search_term.replace(" ","_"), f"img{links.index(link)}")
        url = link.get('href')
        img = session.get(url, headers=headers)
        open(fname,"wb+").write(img.content)
        view(fname)
        input("Continue? ('Enter')\n")
except:
    sys.exit("Bye!")
finally:
    shutil.rmtree(search_term.replace(" ", "_"))
