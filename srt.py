#!/usr/bin/python3
import os
import sys
import shutil
import time
import re
import glob
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Subtitles:

    def __init__(self,DEBUG=False):
        self.url = f"https://www.opensubtitles.org/en/search2/sublanguageid-eng/moviename-"
        self.target = os.getcwd()

        options = Options()
        options.add_argument("--window-size=1366,768")
        options.add_argument("--log-level=3")
        
        options.add_experimental_option('prefs',  {
            "download.default_directory": self.target,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        if not DEBUG:
            options.add_argument("--headless")    
        
        self.browser = webdriver.Chrome(options=options)
    
    def search(self,title,season='',episode=''):
        if season and episode:
            try:
                if int(season) < 10:
                    season = '0' + season
                if int(episode) < 10:
                    episode = '0' + episode
            except:
                self.browser.quit()
                sys.exit("Bad inputs!")
            else:
                self.url += f"{title}+s{season}e{episode}"
        else:
            self.url += f"{title}"
        
        self.browser.get(self.url)

        result_set = self.browser.find_elements_by_class_name('bnone')

        for index,result in enumerate(result_set,1):
            output = result.text
            full_description = result.find_element_by_xpath("./../..").text
            desc = re.findall(r"\[(\w+)\]",full_description)
            if desc:
                output += ' - '+desc[0]
            print(index,' - ',output)
        
        choice = int(input("Enter your choice:\n> ")) - 1
        
        result_set[choice].click()
        print("\nDownloading zip file...\n")
        time.sleep(3)
        self.browser.find_elements_by_xpath("//td[@align='center']/a")[1].click()
        time.sleep(3)
        self.unzip()
    
    def unzip(self):
        self.browser.quit()
        print("\nDownload finished. Unzipping 'srt' file...\n")
        contents = os.listdir(self.target)
        contents = list(filter(lambda x : '.zip' in x,contents))

        for archive in contents:
            shutil.unpack_archive(archive)
            os.remove(archive)
            os.remove(glob.glob("*.nfo")[0])

def setup():
    global srt
    if 'debug' in sys.argv:
        srt = Subtitles(DEBUG=True)
    else:
        srt = Subtitles()
    return

if __name__ == '__main__':
    try:
        srt = None
        init_thread = Thread(target=setup)
        init_thread.start()

        title = input("Enter the name of the series/movie:\n> ")
        season = input("Enter the season number (applicable to series only, leave blank otherwise)\n> ")
        episode = input("Enter the episode number (applicable to series only, leave blank otherwise)\n> ")

        if init_thread.is_alive():
            init_thread.join()

        srt.search(title,season,episode)
    finally:
        try:
            srt.browser.quit()
        except:
            pass
