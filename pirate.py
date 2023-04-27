#!/usr/local/bin/python3
import os
import requests
import sys
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from threading import Thread
from open_apps import start

browser = None
mirrors = []
headers = {'User-Agent': 'masterbyte'}
domain = ""

def init():
    global browser
    op = Options()
    op.headless = True
    log_path = os.path.devnull
    browser = webdriver.Firefox(options=op, service_log_path=log_path)

def populate_mirrors():
    global mirrors
    r = requests.get("https://piratebayproxy.net/")
    s = BeautifulSoup(r.text, 'html.parser')
    mirrors = list(map(lambda x: x.get('href'), s.findAll('a', {'rel': 'nofollow'})))

def choose_mirror():
    global mirrors
    global domain

    mirror = None
    try:
        mirror = mirrors.pop(0)
        print(f"\nTrying {mirror} ...")
        r = requests.get(f"{mirror}/search/{goods}", headers=headers, timeout=7)
        if not r.ok or 'blocked' in r.text or r.text == '':
            raise Exception
        else:
            print(f"\nYay! {mirror} is working ...\n")
            domain = mirror
            return
    except Exception as e:
        print(e)
        if len(mirrors) > 0:
            print(f"\n{mirror} not working ... Choosing again from : \n{mirrors}")
            choose_mirror()
        else:
            exit("You have serious bad luck! Bye!")

def debug(*args,**kwargs):
    while(True):
        try:
            cmd=input("Enter the commands BOSS!\n")
            if cmd=='exit':
                return
            exec(cmd)
        except:
            print('NOT WORKING!')
            pass

if __name__ == '__main__':
    try:
        if len(sys.argv[1:]) < 1:
            raise IndexError
        goods = ' '.join(sys.argv[1:])
    except IndexError:
        exit("Usage : pirate.py [goods]")

    t = Thread(target=init)
    t.start()

    populate_mirrors()
    choose_mirror()
    base_url = f"{domain}"

    if t.is_alive():
        t.join()

    if not browser:
        exit('Issue with Selenium setup. Closing...')
        quit()

    browser.get(f"{base_url}/search/{goods}")
    source = browser.page_source
    browser.quit()

    s = BeautifulSoup(source,'html.parser')
    links = s.select('tr:not(.header)')

    for link in links[:15]:
        try:
            torrent_info_loc = link.select('td')[1]
            print("\n<<< "+str(links.index(link) + 1)+" >>> : TITLE : ", torrent_info_loc.find('a', attrs={'class': 'detLink'}).text)
            print("TORRENT PAGE URL : ", torrent_info_loc.find('a', attrs={'class': 'detLink'}).get('href'))
            print("DESCRIPTION : ", torrent_info_loc.find('font', attrs={'class': 'detDesc'}).text)
            print("MAGENT LINK : ", torrent_info_loc.select('a[href^="magnet"]')[0].get('href'))
            time.sleep(0.5)
        except:
            pass
    
    while True:
        ch = input("\nEnter the number...\n> ")

        mlink = links[int(ch) - 1].select('a[href^="magnet"]')[0].get('href')
        print("Opening : ", mlink)

        # Popen(["qbittorrent",mlink],stdout=PIPE,stderr=PIPE)
        start("qbittorrent", mlink)

