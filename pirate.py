#!/usr/bin/python3
import requests
import sys
import random
from bs4 import BeautifulSoup
from subprocess import Popen, PIPE
from fake_useragent import UserAgent

try:
    if len(sys.argv[1:]) < 1:
        raise IndexError
    goods = ' '.join(sys.argv[1:])
except IndexError:
    exit("Usage : pirate.py [goods]")

mirrors = ["thepiratebay.org", "pirateproxy.ink",
           "thepiratebay.guru", "thepiratebayproxy.info"]
headers = {'User-Agent': UserAgent().random}
data = {'uploaders': [], 'titles': [],
        'magnetLinks': [], 'webpages': [], 'time': []}
r = ''


def choose_mirror():
    global mirrors
    global r
    mirror = random.choice(mirrors)
    mirrors.remove(mirror)
    try:
        print(f"\nTrying {mirror} ...")
        r = requests.get(
            f"http://{mirror}/search/{goods}", headers=headers, timeout=7)
        if not r.ok or 'blocked' in r.text or r.text == '':
            raise Exception
        else:
            print(f"\nYay! {mirror} is working ...\n")
            return
    except:
        if len(mirrors) > 0:
            print(f"\n{mirror} not working ... Choosing again from : \n{mirrors}")
            choose_mirror()
        else:
            exit("You have serious bad luck! Bye!")

choose_mirror()
    
base_torrent_url = r.url[:r.url.find('search')-1]

torrent_data = { 'title' : [], 'torrent_url' : [] }

d = BeautifulSoup(r.text,'html.parser').findAll('a',{'class':'detLink'})

torrent_data['title'] = list(map(lambda x : x.text, d))
torrent_data['torrent_url'] = list(map(lambda x : base_torrent_url+x.get('href'), d))

for link in torrent_data['torrent_url'][:10]:
    try:
        print("\n<<< "+str(torrent_data['torrent_url'].index(link) + 1)+" >>> : TITLE : ",
                torrent_data['title'][torrent_data['torrent_url'].index(link)])
        tp = requests.get(link,headers=headers)
        s = BeautifulSoup(tp.text,'html.parser')
        print("SIZE : ",s.find('dl', {'class': 'col1'}).findAll('dd')[2].text)
        print("UPLOADED ON : ",s.find('dl',{'class':'col2'}).findAll('dd')[0].text)
        print("UPLOADED BY : ",s.find('dl',{'class':'col2'}).findAll('dd')[1].text)
        print("MAGENT LINK : ",s.find('div',{'class':'download'}).find('a').get('href'))
        print("TORRENT PAGE URL : ",tp.url)
        time.sleep(0.5)
    except:
        pass



