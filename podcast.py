#!/usr/bin/python3
import selenium,sys,time
from threading import Thread
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

class GPod:
    def __init__(self):
        options = Options()
        options.headless = True

        if 'linux' in sys.platform:
            if len(sys.argv[1:]) >= 1:
                print("Debug mode on...")
                self.browser = webdriver.Firefox(service_log_path='/dev/null')
            else:
                self.browser = webdriver.Firefox(options=options,service_log_path='/dev/null')
        else:
            if len(sys.argv[1:]) >= 1:
                print("Debug mode on...")
                self.browser = webdriver.Firefox(service_log_path='NUL')
            else:
                self.browser = webdriver.Firefox(options=options,service_log_path='NUL')

    def search(self,pname):
        self.url = f"http://podcasts.google.com/?q={pname}"
        self.browser.get(self.url)
        time.sleep(2)
        self.browser.find_element_by_class_name("YJdYTd").click()
        time.sleep(3)

        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        episodes = self.browser.find_elements_by_class_name('D9uPgd')[::-1]
        for index,epi in enumerate(episodes,1):
            if len(epi.text) > 0:
                print("\n<<< ",str(index)," >>>"' - ',epi.text,'\n')
        ch = int(input("\nEnter the episode number you want to listen to...\n> "))
        episodes[ch-1].click()
        time.sleep(3)
        self.player()

    def player(self):
        def time_left():
            print("\n"+self.browser.find_elements_by_class_name('MBPL8b')[1].text+"\n")

        print(f"\nName : {self.browser.find_element_by_class_name('JCi0he').text}")
        print(f"\nDate and duration : {self.browser.find_element_by_class_name('II6i7d').text}")
        print(f"\nDescription : {self.browser.find_element_by_class_name('OoINtf').text}")
        self.browser.find_element_by_class_name("Cd8jxe").click()

        while True:
            ctrl = input("\n'1' : Play/Pause\n'2' : Rewind 10 seconds\n'3' : Forward 10 seconds\n'4' : Check time left\n'5' : Listen to another podcast\n'6' : Quit\nChoose from above...\n> ")
            if ctrl == '1':
                self.browser.find_element_by_class_name("Cd8jxe").click()
            elif ctrl == '2':
                self.browser.find_elements_by_class_name("U26fgb")[7].click()
            elif ctrl == '3':
                self.browser.find_elements_by_class_name("U26fgb")[9].click()
            elif ctrl == '4':
                time_left()
            elif ctrl == '5':
                pname = input("\nEnter the name of the podcast...\n> ")
                self.search(pname)
            else:
                self.browser.quit()
                exit("See you again!")

if __name__ == '__main__':
    gp = None
    def init():
        global gp
        gp = GPod()

    t = Thread(target=init)
    t.start()
    pname = input("Enter the name of the podcast...\n> ")
    if t.isAlive():
        t.join()

    gp.search(pname)
