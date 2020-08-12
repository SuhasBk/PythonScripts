#!/usr/bin/python3
import requests
import sys
import random
import time
from bs4 import BeautifulSoup
from subprocess import Popen, PIPE
from fake_useragent import UserAgent
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from threading import Thread
from open_apps import start

browser = None
mirrors = ["thepiratebay.org", "pirateproxy.ink"]
headers = {'User-Agent': UserAgent(verify_ssl=False).random}
domain = ""

def init():
    global browser
    op = Options()
    op.headless = True
    log_path = "NUL" if sys.platform.startswith('win') else "/dev/null"
    browser = webdriver.Chrome(options=op, service_log_path=log_path)

def choose_mirror():
    global mirrors
    global domain
    mirror = random.choice(mirrors)
    mirrors.remove(mirror)

    try:
        print(f"\nTrying {mirror} ...")
        r = requests.get(f"http://{mirror}/search.php?q={goods}", headers=headers, timeout=7)
        if not r.ok or 'blocked' in r.text or r.text == '':
            raise Exception
        else:
            print(f"\nYay! {mirror} is working ...\n")
            domain = mirror
            return
    except:
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

    choose_mirror()
    base_url = f"http://{domain}"

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

    ch = input("\nEnter the number...\n> ")

    mlink = links[int(ch) - 1].select('span a')[3].get('href')
    print("Opening : ",mlink)

    # Popen(["qbittorrent",mlink],stdout=PIPE,stderr=PIPE)
    start("qbittorrent",mlink)

