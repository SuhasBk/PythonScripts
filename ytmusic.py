#!/usr/local/bin/python3
import os
import sys
import time
import argparse
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FireOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from msedge.selenium_tools import Edge, EdgeOptions

class YTMusic:

    def __init__(self, args):
        USER_BROWSER = args.browser.lower()
        DEBUG_MODE = args.debug

        if USER_BROWSER == 'firefox':
            opt = FireOptions()
            opt.headless = True

            try:
                if DEBUG_MODE == 'on':
                    print("Debugging mode turned ON...")
                    self.browser = webdriver.Firefox(service_log_path=os.path.devnull)
                else:
                    raise IndexError
            except IndexError:
                self.browser = webdriver.Firefox(options=opt,service_log_path=os.path.devnull)

        elif USER_BROWSER == 'chrome':
            opt = ChromeOptions()
            opt.add_argument("--log-level=3")
            opt.add_argument("--window-size=1366,768")

            if DEBUG_MODE == 'on':
                print("Debugging mode turned ON...")
            else:
                opt.add_argument("--headless")
        
            self.browser = webdriver.Chrome(options=opt,service_log_path=os.path.devnull)

        elif USER_BROWSER == 'edge':
            opt = EdgeOptions()
            opt.use_chromium = True

            opt.add_argument("--log-level=3")
            opt.add_argument("--window-size=1366,768")
            opt.set_capability
            del opt.capabilities['platform']

            if DEBUG_MODE == 'on':
                print("Debugging mode turned ON...")
            else:
                opt.add_argument('--headless')
            
            self.browser = Edge(options=opt, service_log_path=os.path.devnull)
        
        self.browser.get("http://music.youtube.com/")
        
    
    def search_and_play(self, artist):
        # get results
        self.browser.find_element_by_xpath('//*[@id="placeholder"]').click()
        self.browser.find_elements_by_xpath('//*[@id="input"]')[1].send_keys(artist + Keys.ENTER)
        time.sleep(3)

        # sort by artist
        self.browser.find_element_by_xpath("//*[@class='yt-simple-endpoint style-scope ytmusic-chip-cloud-chip-renderer'][@title='Show artist results']").click()
        time.sleep(3)

        # select first artist
        self.browser.find_elements_by_xpath("//*[@class='yt-simple-endpoint style-scope ytmusic-responsive-list-item-renderer']")[0].click()
        time.sleep(3)

        # blast the fuckin' radio!
        # self.browser.find_element_by_xpath('//*[@id="header"]/ytmusic-immersive-header-renderer/div/div/div/div[2]/div/div/yt-button-renderer[2]').find_element_by_tag_name('a').click()

        # Shuffle artist songs
        shuffle_button = self.browser.find_element_by_css_selector('paper-button[aria-label="Shuffle"]')
        try:
            shuffle_button.click()
        except:
            self.browser.execute_script("arguments[0].click()", shuffle_button)
            
    def prev_song_or_rewind(self):
        self.browser.find_element_by_css_selector('tp-yt-paper-icon-button[title="Previous song"]').click()
    
    def play_or_pause(self):
        self.browser.find_element_by_xpath('//*[@id="play-pause-button"]').click()
    
    def next_song(self):
        self.browser.find_element_by_css_selector('tp-yt-paper-icon-button[title="Next song"]').click()
    
    def print_track_info(self):
        track_name = self.browser.find_element_by_xpath('//*[@id="layout"]/ytmusic-player-bar/div[2]/div[1]/yt-formatted-string').text.strip()
        album_name = self.browser.find_element_by_xpath('//*[@id="layout"]/ytmusic-player-bar/div[2]/div[1]/span/span[2]/yt-formatted-string/a[2]').text.strip()
        year = self.browser.find_element_by_xpath('//*[@id="layout"]/ytmusic-player-bar/div[2]/div[1]/span/span[2]/yt-formatted-string/span[3]').text.strip()
        time = self.browser.find_element_by_xpath('//*[@id="left-controls"]/span').text.strip()

        print(f'\nTrack Name: {track_name}\nAlbum Name: {album_name}\nYear: {year}\nTime: {time}\n')
    
    def quit(self):
        self.browser.quit()
        sys.exit("\nHope you had fun! See you around! 😇")
    
def debug(*args, **kwargs):
    while(True):
        try:
            cmd = input("Enter the debugging commands...\n")
            if cmd == 'exit' or cmd == '':
                return
            exec(cmd)
        except Exception as e:
            print('\nBAD CODE\n', e)
            pass


def get_artist_name():
    return input("\nEnter the name of the artist!\n> ")


def initialize(sys_args):
    global ytmusic
    try:
        ytmusic = YTMusic(sys_args)
    except:
        sys.exit(f"Please download correct driver version for {sys_args.browser} and put it in PATH!")
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="  Browser choice and debug mode")
    parser.add_argument("-b", "--browser", type=str, metavar='', required=True, help="firefox / chrome / edge")
    parser.add_argument("-d", "--debug", type=str, metavar='', required=True, help="on / off")
    sys_args = parser.parse_args()

    try:
        ytmusic = None

        init = Thread(target=initialize, args=(sys_args,))
        init.start()

        artist_name = get_artist_name()
        print(f"\nSearching for {artist_name}...\n")

        #  if Python's too slow, wait for it ;)
        if init.is_alive() or not ytmusic:
            print("\nPlease wait, connecting to YouTube Music...\n")
            init.join()

        ytmusic.search_and_play(artist_name)

        options = {
            '1': { 
                'desc': 'Search for a different artist...',
                'op': ytmusic.search_and_play
            },
            '2': {
                'desc': 'Pause / Resume playback',
                'op': ytmusic.play_or_pause
            },
            '3': {
                'desc': 'Play previous song',
                'op': ytmusic.prev_song_or_rewind
            },
            '4': {
                'desc': 'Play current song from 0:00',
                'op': ytmusic.prev_song_or_rewind
            },
            '5': {
                'desc': 'Play next song',
                'op': ytmusic.next_song
            },
            '6': {
                'desc': 'Get current track info',
                'op': ytmusic.print_track_info
            },
            '7': {
                'desc': 'Stop playback and quit',
                'op': ytmusic.quit
            }
        }

        while True:
            for index in options:
                print(f"\n{index}: {options[index]['desc']}")

            choice = input("\nEnter your choice:\n> ")

            if not choice.isnumeric or choice not in options:
                print("\nBad input\n")
            elif choice == '1':
                options[choice]['op'](get_artist_name())
            elif choice in ['4', '5']:
                options[choice]['op']()
                if choice == '4':
                    options[choice]['op']()
            else:
                options[choice]['op']()


    except Exception as e:
        print(e, e.with_traceback)
        if sys_args.debug:
            debug(ytmusic)
            
    finally:
        try:
            ytmusic.browser.quit()
        except:
            pass
        sys.exit("Thank you for using this software. Keep rockin' 🎵🤘🎵")
