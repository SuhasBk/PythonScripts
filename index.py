#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import webbrowser
from subprocess import Popen,PIPE
import sys

try:
    name = ' '.join(map(str,sys.argv[1:]))
except IndexError:
    name=input("Enter the Movie / TV series name:\n")

r=requests.get("http://google.com/search?q=index+of+"+'+'.join(name.split()))

s=BeautifulSoup(r.text,'html.parser')

a=s.select('a')

l=[]
for i in a:
    if name.split()[0].capitalize() in i.text:
        l.append([i.text,i.get("href")[i.get("href").find("http"):i.get("href").find('&sa')].replace('%2520',' ')])

l_backup=l

for i,j in enumerate(l):
    try:
        print((str(i)+' - '+j[0]))
    except:
        pass

ch=eval(input("Enter your choice\n"))

for i,j in enumerate(l_backup):
    if ch == i:
        print(("The link you are requesting is: "+j[1]))
        r1=requests.get(j[1])

        if r1.ok:
            print("\n\nThe link seems to be legit\n")
            s1=BeautifulSoup(r1.text,'html.parser')
            a1=s1.select('a')

            a1_backup=a1[:]

            for p,q in enumerate(a1):
                print((str(p)+' >>> '+r1.url+q.get('href')))

            ch1 = input("\nEnter the choice:\n> ")

            for p,q in enumerate(a1_backup):
                if ch1==str(p):
                    link=r1.url+q.get('href')
                    operation=input("\nDo you want to download (type 'd') or open the website? (type 'w') or stream media using VLC? (type 'v')\n").lower()

                    if operation == 'w':
                        print("Loading...\n")
                        webbrowser.open(j[1])

                    elif operation == 'd':
                        print(("\nPlease wait... Downloading..."+link))
                        Popen(["youtube-dl",link])

                    elif operation == 'v':
                        print(("Streaming... "+link))
                        try:
                            Popen(['vlc',link],stderr=PIPE,stdout=PIPE,close_fds=True)
                        except FileNotFoundError:
                            Popen([input("Enter your default media player...\nEx: 'mpv','totem' : "),link],stderr=PIPE,stdout=PIPE,close_fds=True)
        else:
            print("The link is broken... Try other links..\n")
            exit()
