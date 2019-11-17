#!/usr/bin/python3
import requests,sys
from bs4 import *
import clipboard
from subprocess import *

try:
    if len(sys.argv[1:]) < 1:
        raise IndexError
    goods = ' '.join(sys.argv[1:])
except IndexError:
    exit("Usage : pirate.py [goods]")

# THE ULTIMATE DATA STRUCTURE IN PYTHON:
data={'uploaders':[],'titles':[],'magnetLinks':[],'webpages':[],'time':[]}

def disp():
    for i,j in enumerate(data['titles'][:20]):
        try:
            print('\n',i,' - ',j,'\n',data['time'][i])
        except:
            pass
    print('\n')
    ch=input("Enter the choice ('exit' to quit)\n")
    if ch=='exit':
        exit()
    ch=int(ch)
    return(data['uploaders'][ch], data['webpages'][ch], data['magnetLinks'][ch])

try:
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'}
    r=requests.get("https://thepiratebay.org/search/"+goods+"/0/99/0",headers=headers)
except:
    exit("Service not available right now..")

if 'blocked' in r.text:
    print("Oops! It appears as if this website is inaccessible... Sorry, mate!")
    exit()

a = BeautifulSoup(r.text,'html.parser').select('a')
descs = BeautifulSoup(r.text,'html.parser').select('font')
for desc in descs:
    data['time'].append(desc.text.split(',')[0].upper())

for i in a:
    if 'detDesc' in str(i.get('class')):
        data['uploaders'].append(str(i.text))

    if 'detLink' in str(i.get('class')):
        data['titles'].append(i.text)

    if 'magnet' in i.get("href"):
        data['magnetLinks'].append((i.get('href')))

    if '/torrent/' in i.get('href'):
        data['webpages'].append(i.get('href'))

def info():
    print(("Uploaders : "+str(len(data['uploaders']))))
    print(("Titles : "+str(len(data['titles']))))
    print(("Magnet Links : "+str(len(data['magnetLinks']))))
    print(("Webpages : "+str(len(data['webpages']))))
    if len(data['titles']) > 1:
        return True
    else:
        return False

if(info()):
    pass
else:
    exit("Something's wrong nibba!")

try:
    choice=disp()
    url = 'https://thepiratebay.org'+choice[1]
    s=requests.get(url,headers={'user-agent':'random_stuff'})
    page = BeautifulSoup(s.text,'html.parser')
    com = page.find('div',attrs={'id':'comments'}).text
    size = page.findAll('dd')[2].text if page.findAll('dd')[2]!=None else 'NaN'
    uploaded = page.find('dl',attrs={'col2'}).find('dd').text if page.find('dl',attrs={'col2'}).find('dd') != None else 'NaN'
    print('Uploader : '+choice[0]+'\n\nURL : '+url+'\n\nSize : '+size+'\n\nUploaded on : '+uploaded+'\n\nMagnet Link : '+choice[2]+'\n\nComments : \n'+com)
    clipboard.copy(choice[2])
    if sys.platform == 'linux':
        Popen(['qbittorrent',choice[2]],stdout=PIPE,stderr=PIPE,close_fds=True)

except KeyboardInterrupt:
    quit()
