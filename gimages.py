#!/usr/bin/python3
import selenium,sys,os,shutil,re,requests,webbrowser
from subprocess import *
from threading import Thread
from bs4 import *
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

browser = None

def init():
    global browser
    options = Options()
    options.headless = True

    if 'linux' in sys.platform:
        browser = webdriver.Firefox(options=options,service_log_path='/dev/null')
    else:
        browser = webdriver.Firefox(options=options,service_log_path='NUL')

def view(path):
    if 'linux' in sys.platform:
        p = Popen("xdg-open",path)
    else:
        webbrowser.open(path)

def fetch(search_term):
    global browser
    browser.get(f"https://www.google.com/search?tbm=isch&q={search_term}")

    source = BeautifulSoup(browser.page_source,'html.parser')
    browser.quit()

    images = source.findAll('img',attrs={'data-src':re.compile(r'[\w+]')})

    for i in images[:int(len(images)*0.15)]:
        url = i.get('data-src')

        im = requests.get(url)
        path = 'img{}.jpg'.format(images.index(i+1))
        with open(path,"wb+") as f:
            f.write(im.content)
        
        view(path)
        input("Press 'enter' to see next image...\n")

if __name__ == '__main__':        
    try:
        t = Thread(target=init)
        t.start()

        if len(sys.argv[1:]) > 0:
            search_term = '+'.join(sys.argv[1:])
        else:
            search_term = input("Enter the search term\n> ")

        if t.isAlive():
            print(f"Searching for {search_term}...")
            t.join()

        os.mkdir(search_term)
        os.chdir(search_term)
        fetch(search_term)
    except Exception as e:
        print(e)
    finally:
        os.chdir("..")
        shutil.rmtree(search_term)
        exit("Thank you for using!")
