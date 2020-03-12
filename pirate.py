#!/usr/bin/python3
import requests,sys
from bs4 import BeautifulSoup
import clipboard
from subprocess import Popen,PIPE

try:
    if len(sys.argv[1:]) < 1:
        raise IndexError
    goods = ' '.join(sys.argv[1:])
except IndexError:
    exit("Usage : pirate.py [goods]")

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'}
data={'uploaders':[],'titles':[],'magnetLinks':[],'webpages':[],'time':[]}

try:
    print(f"Searching for {goods}...\nTrying first server...")
    r = requests.get(f"https://thepiratebay.org/search/{goods}",headers=headers,timeout=5)
except requests.exceptions.ReadTimeout:
    print("\nFailed!!! Trying second server...")
    r = requests.get(f"https://pirateproxy.ink/search/{goods}",headers=headers)
    if not r.ok:
        exit("Servers are down! :(")
    
url = r.url[:r.url.find('search')-1]
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

def disp():
    for i, j in enumerate(data['titles'][:20]):
        try:
            print('\n', i, ' - ', j, '\n', data['time'][i])
        except:
            pass
    print('\n')
    ch = input("Enter the choice ('exit' to quit)\n")
    if ch == 'exit':
        exit()
    ch = int(ch)
    return(data['uploaders'][ch], data['webpages'][ch], data['magnetLinks'][ch])

if(info()):
    pass
else:
    exit("Something's wrong nibba!")

while True:
    choice = disp()
    s = requests.get(url+choice[1], headers=headers)
    page = BeautifulSoup(s.text,'html.parser')
    com = page.find('div',attrs={'id':'comments'}).text
    size = page.findAll('dd')[2].text if page.findAll('dd')[2]!=None else 'NaN'
    uploaded = page.find('dl',attrs={'col2'}).find('dd').text if page.find('dl',attrs={'col2'}).find('dd') != None else 'NaN'
    print('Uploader : '+choice[0]+'\n\nURL : '+s.url+'\n\nSize : '+size+'\n\nUploaded on : '+uploaded+'\n\nMagnet Link : '+choice[2]+'\n\nComments : \n'+com)
    clipboard.copy(choice[2])
    if sys.platform == 'linux':
        Popen(['qbittorrent',choice[2]],stdout=PIPE,stderr=PIPE,close_fds=True)
