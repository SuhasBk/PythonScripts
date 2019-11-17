#!/usr/bin/python3
import selenium,time,os,sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import *
from getpass import getpass
from threading import Thread

def debug():
    while(True):
        try:
            cmd=input("Enter the debugging commands...\n")
            if cmd=='exit' or cmd=='':
                return
            exec(cmd)
        except:
            print('\nBAD CODE\n')
            pass
def spinner():
    t = ('|','/','-','\\')
    for i in t:
        print('\r',i,end='')
        time.sleep(0.1)

def login():
    b.get("http://instagram.com/accounts/login")
    time.sleep(2)
    form = b.find_elements_by_class_name('_2hvTZ')
    form[0].send_keys(input("Enter the username:\n> "))
    form[1].send_keys(getpass("Enter the password:\n> ")+Keys.TAB+Keys.ENTER)

    notif_found = False
    while not notif_found:
        try:
            b.find_element_by_class_name('HoLwm').click()
            notif_found = True
        except:
            pass

def retrieve(data,extra=False):
    data.click()
    payload = set()
    time.sleep(2)
    k = b.find_element_by_class_name('isgrP')
    k.click()

    for i in range(500):
        time.sleep(0.1)
        k.send_keys(Keys.DOWN)

    s = BeautifulSoup(b.page_source,'html.parser')
    f = s.findAll('a',attrs={'class':'_0imsa'})
    for i in f:
        if extra:
            if 'verified' in i.find_all_next()[0].text.lower():
                continue
        payload.add(i.text)
    b.find_element_by_class_name('wpO6b').click()
    return payload

def fill_followers():
    global followers
    followers = retrieve(b.find_elements_by_class_name('g47SY')[1])

def fill_following():
    global following
    following = retrieve(b.find_elements_by_class_name('g47SY')[2],extra=True)

if __name__ == '__main__':
    followers=set()
    following=set()
    opt = Options()
    opt.headless = True
    #b = webdriver.Firefox(options=opt)
    b = webdriver.Firefox()
    login()
    print("\nLogged in successfully!\n")
    b.get("http://instagram.com/suhasbk/")
    print("Getting followers list...(may take upto a minute)\n")
    t1 = Thread(target=fill_followers)
    t1.start()
    while t1.isAlive():
        spinner()
    print("\rGetting following list...(may take upto a minute)\n")
    t2 = Thread(target=fill_following)
    t2.start()
    while t2.isAlive():
        spinner()
    losers = following-followers
    print(f"\r\nDifference = {len(following)} - {len(followers)} = {len(losers)}\nAccounts not following back :\n")
    for l in losers:
        print(l)
    b.quit()
    try:
        os.remove('geckodriver.log')
    except:
        pass
