#!/usr/bin/python3
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,os,re,sys

class WhatsApp:
    def __init__(self):
        if 'linux' in sys.platform:
            url = os.path.join(os.environ['HOME'], '.mozilla', 'firefox')
        else:
            url = os.path.join(os.environ.get('HOMEPATH'),'AppData','Roaming','Mozilla','Firefox','Profiles')

        l = os.listdir(url)
        profile = list(filter(lambda x: '.default-release' in x, l)).pop()
        profile = os.path.join(url, profile)

        print(("Using profile ID : {}".format(profile)))
        fp = webdriver.FirefoxProfile(profile)
        self.browser = webdriver.Firefox(firefox_profile=fp)
        self.browser.get("https://web.whatsapp.com")
        self.browser.minimize_window()
    
    def search(self,contact):
        self.contact = contact
        found = False

        self.browser.find_element_by_xpath("//div[@title='New chat']").click()

        search_bar = self.browser.find_element_by_class_name('_2S1VP')
        search_bar.click()
        search_bar.send_keys(self.contact)

        results = self.browser.find_element_by_xpath("//div[@class='_1vDUw _2sNbV']")
        l = results.find_elements_by_class_name('_3NFp9')

        for index, cont in enumerate(l,1):
            print(index,' - ',cont.text)
        
        ch = int(input("\nEnter the contact number corresponding to the contact...\n> "))
        l[ch-1].click()

        self.DONE = True

            
    def chat(self):
        pass



if __name__ == '__main__':
    wapp = WhatsApp()

    contact = input("Enter the contact to search...\n> ")
    wapp.search(contact)
    
    wapp.chat()


