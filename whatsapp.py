#!/usr/bin/python3
import sys
import selenium
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WhatsApp:

    def debug(self,*args,**kwargs):
        while(True):
            try:
                cmd = input("Enter the debugging commands...\n")
                if cmd == 'exit' or cmd == '':
                    return
                exec(cmd)
            except:
                print('\nBAD CODE\n')
                pass

    def wait_and_find(self, elements, selector, root=None, time=10):
        if root==None:
            root = self.browser

        for element in elements:
            try:
                WebDriverWait(self.browser,time).until(EC.element_to_be_clickable((selector,element)))
                return root.find_elements(selector, element)
            except TimeoutException:
                pass
        
        return []
    
    def check_contact(self):
        if self.contact == '':
            print("\nOpen a new chat with a contact first!\n")
            return False
        return True


    def __init__(self,use_default_profile=False):
        print("Initializing WhatsApp...\n\nPlease keep your phone nearby and unlocked for a hassle-free experience...")

        self.contact = ''

        if use_default_profile:
            fp = webdriver.FirefoxProfile("/home/gandalf/.mozilla/firefox/39eqzx5x.default-release")
            self.browser = webdriver.Firefox(firefox_profile=fp,service_log_path='/dev/null')
        else:
            self.browser = webdriver.Firefox(service_log_path="/dev/null")
        self.browser.get("https://web.whatsapp.com/")

    def login(self):
        banner = self.wait_and_find(['_1u3Tz'],By.CLASS_NAME)
        
        while len(banner) > 0:
            try:
                self.browser.refresh()
                banner = self.wait_and_find(['_1u3Tz'], By.CLASS_NAME)
                self.browser.execute_script("alert('Please scan the QR code from the app...')")
                sleep(10)
            except:
                pass
        
        #self.browser.minimize_window()
    
    def open_chat(self, contact_name=None, emergency_mode=False):
        if emergency_mode and contact_name!=None:
            self.contact = contact_name
        else:
            contact_name = input("Enter the contact name...\n> ")
        
        self.wait_and_find(["//div[@role='button'][@title='New chat']"],By.XPATH)[0].click()
        search_bar = self.wait_and_find(['_2S1VP', '_3FRCZ'], By.CLASS_NAME, self.browser,5)
        search_bar[0].send_keys(contact_name)
        sleep(2)
        contacts_list = self.wait_and_find(['_2xoTX'],By.CLASS_NAME,self.browser,5)[0]
        contact_links = self.wait_and_find(['_2kHpK'],By.CLASS_NAME,contacts_list,5)

        if emergency_mode:
            contact_links[0].click()
        else:
            False
            for index,contact in enumerate(contact_links,1):
                print(index,' : ',' ---> '.join(contact.text.split('\n')))

            ch = int(input("\n\nWhich "+contact_name+"?\n> ")) - 1

            contact_links[ch].click()
        self.contact = contact_name
    
    def chat_info(self):
        if not self.check_contact():
            return
        
        if len(self.wait_and_find(["//span[@title='online']"],By.XPATH,self.browser,3)) == 1:
            print(f"\nYay! The {self.contact} appears to be online!\n")
        else:
            print("\n",self.contact+" appears to be offline ")
        
        try:
            recent_messages = self.wait_and_find(['message-in'],By.CLASS_NAME)

            if len(recent_messages) == 0: raise Exception

            messages = list(map(lambda x : self.wait_and_find(['_3zb-j','_3Whw5'],By.CLASS_NAME,x,2)[0].text, recent_messages))
            time_stamps = list(map(lambda x: self.wait_and_find(['_18lLQ','_3EFt_'],By.CLASS_NAME,x,2)[0].text, recent_messages))
            
            for m, t in zip(messages, time_stamps):
                print("\n",'[',m.upper(),']', ' @ ', t)

        except:
            print("\nUnable to fetch recent messages at this time\n")
    
    def send_message(self,message=None):
        if not self.check_contact():
            return
        sleep(3)
        
        if message==None:
            message= input("Enter the message to be sent...\n> ")

        self.wait_and_find(['_2S1VP','_3FRCZ'],By.CLASS_NAME,self.browser,5)[1].send_keys(message+Keys.ENTER)
        print("\nMessage sent!")
    
    def send_file(self,path=None,file_type=None):
        if not self.check_contact():
            return
        
        if path == None:
            path = input("Enter the ABSOLUTE PATH of the file to send...\n> ")
        if file_type == None:
            file_type = input("Enter the type of file... ('img' or 'file')\n> ")
        
        self.browser.find_element_by_xpath("//div[@title='Attach']").click()
        sleep(0.5)

        inputs = self.browser.find_elements_by_xpath("//input[@type='file']")

        if file_type == 'img':
            inputs[0].send_keys(path)
        elif file_type == 'file':
            inputs[1].send_keys(path)
        else:
            print("Wrong file format!")
            return

        self.wait_and_find(["_3y5oW"],By.CLASS_NAME)[0].click()

def emergency_message(wapp):
    contact, data = sys.argv[1], sys.argv[2]
    wapp.open_chat(contact,True)
    
    try:
        file_type = sys.argv[3]
        wapp.send_file(data, file_type)
    except IndexError:
        wapp.send_message(data)

    print(f"\nYour message has been sent to {contact}")

if __name__ == '__main__':
    try:
        wapp = WhatsApp(True)
        wapp.login()

        if len(sys.argv[1:]) > 0:
            print("Emergency mode turned on...")
            emergency_message(wapp)

        functions = {
            '1' : {
                'function' : wapp.open_chat,
                'description' : "Open new chat with a contact?"
                },
            '2' : {
                'function' : wapp.chat_info,
                'description' : "Get recent chats with current contact?"
                },
            '3': {
                'function' : wapp.send_message,
                'description' : "Send message to current contact?"
                },
            '4' : {
                'function' : wapp.send_file,
                'description' : "Send files to current contact?"
                }
            }

        while True:
            for index,data in functions.items():
                print('\n',index,' : ',data['description'])
            
            op = input("\nWhat do you want to do?\n('quit' to close WhatsApp)\n> ")
            
            if op.lower() != 'quit':
                functions[op]['function']()
            else:
                sys.exit()   
    finally:
        print("Thank you for using WhatsApp CLI. Until next time...")
        wapp.browser.quit()
