#!/usr/bin/python3
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,os,re,sys

def debug():
    while(True):
        try:
            cmd=input("Enter the commands BOSS!\n")
            if cmd=='exit':
                return
            exec(cmd)
        except:
            print('NOT WORKING!')
            pass

def login():
    b.find_element_by_id('pane-side') #class for side pane which is visible only when logged in
    return True

def chat():
    canvas = b.find_element_by_class_name('_9tCEa') #class for chat screen only if a chat has been selected
    return True

def steal():
    try:
        os.mkdir('screenshots')
    except:
        pass
    w=b.find_element_by_class_name('_2nmDZ')   #chat's scrollable element
    w.click()
    for i in range(1,6):
        b.save_screenshot('screenshots/ss{}.png'.format(i)) #save a screenshot after scrolling
        for i in range(1,6):
            w.send_keys(Keys.UP)                #scroll up 6 times
    return

def online():
    online = b.find_elements_by_class_name('O90ur')
    if len(online)==0:
        pass
    else:
        name = b.find_element_by_class_name('_2zCDG').text.upper()
        start = time.time()
        try:
            if 'online' in online[0].text:
                print(("{} was online at : {}".format(name,time.ctime())))
                while 'online' in online[0].text:
                    pass
        except selenium.common.exceptions.StaleElementReferenceException:
            stop = time.time()
            diff=int(stop-start)
            if diff!=0:
                print(("{} was approx. online for : {} seconds!".format(name,diff)))
            pass
    return

def new_chat():
    searchbar = b.find_element_by_class_name('jN-F5')
    searchbar.click()
    searchbar.send_keys(input("Enter the contact's name:\n> "))
    time.sleep(1)
    searchbar.send_keys(Keys.TAB)
    for i in range(50):searchbar.send_keys(Keys.BACKSPACE)
    debug()
    return

def handler():
    try:
        if login():
            try:
                while True:
                    if chat():
                        #steal()
                        online()
                        #new_chat()
            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(5)
                handler()
    except selenium.common.exceptions.NoSuchElementException:
        time.sleep(2)
        handler()
    except:
        pass


url = os.path.join(os.environ['HOME'],'.mozilla','firefox')
profile = os.path.join(url,os.listdir(url)[3])

print(("Using profile ID : {}".format(profile)))
fp = webdriver.FirefoxProfile(profile)
b=webdriver.Firefox(fp)
b.get("https://web.whatsapp.com")
handler()
