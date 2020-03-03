#!/usr/bin/python3
import selenium,sys,os,shutil,re,requests
from subprocess import *
from threading import Thread
from bs4 import *
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

browser = None
cmd = None

def init():
    global browser
    global cmd
    options = Options()
    options.headless = True

    if 'linux' in sys.platform:
        cmd = "browse"
        browser = webdriver.Firefox(options=options,service_log_path='/dev/null')
    else:
        cmd = "start"
        browser = webdriver.Firefox(options=options,service_log_path='NUL')

def fetch(search_term):
    global browser
    browser.get(f"https://www.google.com/search?tbm=isch&q={search_term}")

    source = BeautifulSoup(browser.page_source,'html.parser')
    browser.quit()

    images = source.findAll('img',attrs={'data-src':re.compile(r'[\w+]')})

    for i in images[:int(len(images)*0.15)]:
        url = i.get('data-src')

        im = requests.get(url)
        path = 'img{}.jpg'.format(images.index(i))
        with open(path,"wb+") as f:
            f.write(im.content)

        p = Popen([cmd,path])
        input("Press 'enter' to see next image...\n")

if __name__ == '__main__':
    if len(sys.argv[1:]) > 0:
        search_term = '+'.join(sys.argv[1:])
    else:
        search_term = input("Enter the search term\n> ")
        
    try:
        t = Thread(target=init)
        t.start()

        if t.isAlive():
            print(f"Searching for {search_term}...")
            t.join()

        os.mkdir(search_term)
        os.chdir(search_term)
        fetch(search_term)
    finally:
        os.chdir("..")
        shutil.rmtree(search_term)
        exit("Thank you for using!")
