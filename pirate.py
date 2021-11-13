#!/usr/local/bin/python3
import os
import requests
import sys
import random
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
    r = requests.get("https://proxybay.github.io/")
    s = BeautifulSoup(r.text, 'html.parser')
    mirrors = list(map(lambda x: x.get('href'), s.findAll('a', {'rel': 'nofollow'})))

def choose_mirror():
    global mirrors
    global domain

    try:
        mirror = mirrors.pop(0)
        print(f"\nTrying {mirror} ...")
        r = requests.get(f"{mirror}/search.php?q={goods}", headers=headers, timeout=7)
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

    browser.get(f"{base_url}/search.php?q={goods}")
    source = browser.page_source
    browser.quit()

    s = BeautifulSoup(source,'html.parser')
    links = s.select('li[id="st"]')

    for link in links[:15]:
        try:
            print("\n<<< "+str(links.index(link) + 1)+" >>> : TITLE : ",link.select('span a')[2].text)
            print("TORRENT PAGE URL : ",base_url+link.select('span a')[2].get('href'))
            print("SIZE : ",link.select('span')[4].text)
            print("UPLOADED ON : ",link.select('span')[2].text)
            print("UPLOADED BY : ",link.select('span')[7].text)
            print("MAGENT LINK : ",link.select('span a')[3].get('href'))
            time.sleep(0.5)
        except:
            pass
    
    while True:
        ch = input("\nEnter the number...\n> ")

        mlink = links[int(ch) - 1].select('span a')[3].get('href')
        print("Opening : ",mlink)

        # Popen(["qbittorrent",mlink],stdout=PIPE,stderr=PIPE)
        start("qbittorrent",mlink)

