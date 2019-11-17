#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,os,sys
from selenium.webdriver.firefox.options import Options

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

options=Options()
options.headless=True
if len(sys.argv[1:]) < 1:
    b = webdriver.Firefox(options=options)
else:
    b = webdriver.Firefox()
try:
    b.get('http://192.168.0.1')
except:
    b.quit()
    exit("The link itself is broken! Can't even access the router's index page!")


def do():
    b.find_element_by_id('userName').send_keys('admin')
    b.find_element_by_id('pcPassword').send_keys('sherlocked'+Keys.ENTER)
    time.sleep(5)

    found = False

    while not found:
        try:
            b.switch_to.frame('bottomLeftFrame')
            found = True
        except:
            print("Testing")
            time.sleep(2)


    time.sleep(1)
    b.find_element_by_id('menu_tools').click()
    time.sleep(1)
    b.find_element_by_id('menu_restart').click()
    b.switch_to.default_content()
    b.switch_to.frame(b.find_elements_by_tag_name('frame')[2])
    time.sleep(1)
    b.execute_script('doRestart();')
    b.switch_to.alert.accept()
    print("Router successfully rebooted!")

try:
    do()
except:
    print("Task failed successfully")
finally:
    b.quit()
    os.remove('geckodriver.log')
    exit()
