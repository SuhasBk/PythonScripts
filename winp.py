#!/usr/bin/python3
import requests
from bs4 import *
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

requests.packages.urllib3.disable_warnings()

base="https://sourceforge.net"

r=requests.get(base+"/directory/os:windows/?q="+'+'.join(input("Enter the open source software name\n").split(' ')),headers={'user-agent':'my-app'},verify=False)

s=BeautifulSoup(r.text,'html.parser')

a=s.findAll('a',attrs={'itemprop':'url'})

for i,j in enumerate(a[2:],1):
    print(str(i),j.text)

ch=eval(input("Enter the choice\n"))

for i,j in enumerate(a[2:],1):
    if ch==i:
        url=base+j.get('href')
        options=Options()
        options.headless=True
        r=requests.get(url)
        s=BeautifulSoup(r.text,'html.parser')
        a=s.find('a',attrs={'class':'button download big-text green '})
        print(base+a.get("href"))
        b=webdriver.Firefox()
        b.get(base+a.get("href"))
