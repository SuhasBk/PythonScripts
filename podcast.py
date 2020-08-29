#!/usr/local/bin/python3
import os
import sys
import time
from threading import Thread
import selenium
from colorama import Back, Fore, Style
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


class GPod:
    def __init__(self):
        options = Options()
        options.headless = True

        if len(sys.argv[1:]) >= 1:
            print("Debug mode on...")
            self.browser = webdriver.Firefox(service_log_path=os.path.devnull)
        else:
            self.browser = webdriver.Firefox(options=options,service_log_path=os.path.devnull)
        
    def choose_class(self,classes):
        class_element = None

        for cls in classes:
            try:
                class_element = self.browser.find_element_by_class_name(cls)
            except selenium.common.exceptions.NoSuchElementException:
                pass

        if class_element == None:
            raise selenium.common.exceptions.NoSuchElementException

        return class_element

    def search(self,pname):
        self.url = f"http://podcasts.google.com/?q={pname}"
        self.browser.get(self.url)        
        time.sleep(2)
        self.choose_class(["ugPjk","YJdYTd"]).click()
        time.sleep(3)

        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        episodes = self.browser.find_elements_by_xpath('//a[@class="D9uPgd"][@jsname="ma59G"]')
        episodes = list(filter(lambda x : len(x.text) > 0,episodes))

        n = int(input("\nEnter the episodes list limit...\n> "))
        
        for index,episode in enumerate(episodes[:n],1):
            lines = episode.text.split('\n')
            print("\n",Back.BLACK,Fore.YELLOW,"<<< ",str(index)," >>>"' - ',lines[1].strip(),Style.RESET_ALL,'\n')
            print("Uploaded on : "+lines[0])
            print('\n'.join(lines[2:]))
            time.sleep(0.8)

        ch = int(input("\nEnter the episode number you want to listen to...\n> "))
        self.browser.execute_script("arguments[0].click()",episodes[ch-1])
        time.sleep(3)
        self.player()            

    def time_left(self):
        print("\n"+self.browser.find_elements_by_class_name('MBPL8b')[1].text+"\n")
        
    def player(self):
        print(f"\nName : {self.choose_class(['JCi0he','wv3SK']).text}")
        print(f"\nDate and duration : {self.choose_class(['II6i7d','Mji2k']).text}")
        print(f"\nDescription : {self.choose_class(['OoINtf','QpaWg','aDrCHe']).text}")
        self.choose_class(["Cd8jxe", "wD7LYe"]).click()

        while True:
            ctrl = input("\n'1' : Play/Pause\n'2' : Rewind 10 seconds\n'3' : Forward 30 seconds\n'4' : Check time left\n'5' : Listen to another podcast\n'6' : Quit\nChoose from above...\n> ")
            if ctrl == '1' or ctrl.isspace():
                self.browser.execute_script("arguments[0].click()",self.choose_class(["Cd8jxe", "wD7LYe"]))
            elif ctrl == '2':
                self.browser.find_element_by_xpath('//div[@aria-label="Rewind 10 seconds"]').click()
            elif ctrl == '3':
                self.browser.find_element_by_xpath('//div[@aria-label="Fast forward 30 seconds"]').click()
            elif ctrl == '4':
                self.time_left()
            elif ctrl == '5':
                pname = input("\nEnter the name of the podcast...\n> ")
                self.search(pname)
            else:
                self.browser.quit()
                exit("See you again!")


def init():
    global gp
    gp = GPod()

if __name__ == '__main__':
    try:
        gp = None
        t = Thread(target=init)
        t.start()
        pname = input("Enter the name of the podcast...\n> ")
        if t.is_alive():
            t.join()
        gp.search(pname)
    except Exception as e:
        print(e)
    finally:
        try:
            gp.browser.quit()
        except:
            pass
