#!/usr/bin/python3
import selenium,time,os,sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from getpass import getpass

def debug(msg=""):
    print(f"\nCaught exception : {msg}\n")
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
    b.execute_script("arguments[0].click();",data)
    payload = set()
    time.sleep(2)
    k = b.find_element_by_class_name('isgrP')
    b.execute_script("arguments[0].click()",k)

    for i in range(300):
        time.sleep(0.1)
        try:
            k.send_keys(Keys.DOWN)
        except:
            pass

    s = BeautifulSoup(b.page_source,'html.parser')
    f = s.findAll('a',attrs={'class':'_0imsa'})
    for i in f:
        if extra:
            if 'verified' in i.find_all_next()[0].text.lower():
                continue
        payload.add(i.text)

    close_button = b.find_element_by_class_name('wpO6b')
    b.execute_script("arguments[0].click()",close_button)

    return payload

def fill_followers():
    global followers
    followers = retrieve(b.find_elements_by_class_name('g47SY')[1])

def fill_following():
    global following
    following = retrieve(b.find_elements_by_class_name('g47SY')[2],extra=True)

def log_out():
    b.execute_script("arguments[0].click();",b.find_element_by_class_name('wpO6b'))
    options = b.find_element_by_class_name('mt3GC')
    log_out_button = options.find_elements_by_tag_name('button')[8]
    b.execute_script("arguments[0].click();",log_out_button)
    time.sleep(3)
    b.quit()

if __name__ == '__main__':
    followers = set()
    following = set()
    opt = Options()
    opt.headless = True

    if sys.platform == 'linux':
        log_path = '/dev/null'
    else:
        log_path = 'NUL'

    if len(sys.argv) > 1:
        print("Debug mode ON")
        b = webdriver.Firefox(service_log_path=log_path)
    else:
        b = webdriver.Firefox(options=opt,service_log_path=log_path)

    login()
    print("\nLogged in successfully!\n")

    time.sleep(2)
    b.find_element_by_class_name('gmFkV').click()
    time.sleep(2)

    print("Getting followers and following list...(may take upto 2 minutes)\n")

    fill_followers()
    fill_following()

    losers = following-followers
    print("\rAccounts not following back :\n")
    for l in losers:
        print(l)

    log_out()
