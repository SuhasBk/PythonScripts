#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium
import time,string,os,sys

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

if len(sys.argv)>1:
    print("Running in debugging mode...\n")
    b=webdriver.Firefox()
else:
    from selenium.webdriver.firefox.options import Options
    opt=Options()
    opt.headless=True
    b=webdriver.Firefox(options=opt)

b.get("http://1cast.in")
time.sleep(2)
stations = b.find_elements_by_class_name("single-station")[:3]

try:
    while True:
        for i,j in enumerate(['Mumbai', 'Delhi', 'Bangalore'],1):
            print(i,j)

        ch = input("Enter the choice : ('exit' to quit)\n> ")

        for i,j in enumerate(stations,1):
            if ch == str(i):
                j.click()
            elif ch == 'exit':
                exit()
finally:
    b.quit()
    os.remove('geckodriver.log')
