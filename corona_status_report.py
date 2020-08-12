#!/usr/bin/python3

import sys,webbrowser
from requests import Session
from bs4 import BeautifulSoup
from datetime import date
from subprocess import Popen,PIPE
from fake_useragent import UserAgent

s = Session()
r = s.get("https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports", headers={'User-Agent': UserAgent(verify_ssl=False).random})
html = BeautifulSoup(r.text,'html.parser')
pdf_url = html.findAll('div',{'class':'sf-content-block'})[10].find('a').get('href')
full_url = "https://" + r.url.split('/')[2] + pdf_url
p = s.get(full_url)
s.close()

fname = f"{date.today()}_report.pdf"
open(fname, "wb+").write(p.content)
if 'linux' in sys.platform:
    Popen(["xdg-open",fname],stdout=PIPE,close_fds=True)
else:
    webbrowser.open(fname)
