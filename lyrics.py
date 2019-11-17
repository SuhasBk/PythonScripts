#!/usr/bin/python3
import requests
import re
from bs4 import *

while True:
    p=input("Enter the name of the song (avoid artist's name):\n").split()
    r=requests.get("https://search.azlyrics.com/search.php?q="+'+'.join(p),headers={'User-Agent':'MyApp'})

    s=BeautifulSoup(r.text,'html.parser')
    td=s.findAll('td',attrs={'class':'text-left visitedlyr'})
    res=[]

    for i,j in enumerate(td[:5]):
        s=re.findall(r'<b>.*</b>',str(j))[0]
        for r in (('<b>',''),('</b>',''),('</a>','')):
            s=s.replace(*r)
        print(i,s)
        res.append(j.find('a').get('href'))

    ch=eval(input("\nChoose one from above:\n"))

    for i,j in enumerate(res):
        if ch==i:
            q=requests.get(j)
            s=BeautifulSoup(q.text,'html.parser')
            l=s.find('div',attrs={'class':'col-xs-12 col-lg-8 text-center'})
            print(l.find('div',attrs={'class':''}).text)
