#!/usr/bin/python3
artist = '+'.join(input("Enter the song/artist name you want to listen to....\n> ").split())
print('\nWelcome! Connecting to Gaana...Bas bajna chahiye gaana ;)\n')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium
import time,string,sys

if len(sys.argv)>1:
    print("Running in debugging mode...\n")
    b=webdriver.Chrome()
else:
    from selenium.webdriver.firefox.options import Options
    opt=webdriver.ChromeOptions()
    opt.headless=True
    b=webdriver.Chrome(options=opt)

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

def handler():
    try:
        pause = 0
        rep = 0
        while True:
            time.sleep(0.5)
            print(("\nTrack name : "+b.find_element_by_id('stitle').text+' from the album - '+b.find_element_by_id('atitle').text+'\n'))

            ch = input("\n'1' : New Artist\n'2' : Next Song\n'3' : Play/Pause\n'4' : Previous Song\n'5' : Song Info\n'6' : Top Songs(this week)\n'7' : Repeat Current Song\n\nEnter your choice...('exit' to quit)\n> ")

            if ch=='1':
                artist = '+'.join(input("Enter the song/artist name you want to listen to.... Type 'q' to go back\n> ").split())
                if artist == 'q':
                    pass
                else:
                    navigate(artist)

            elif ch=='2':
                try:
                    b.find_element_by_class_name('next-song').click()
                    print("\nPlaying next song...\n")
                except:
                    if len(sys.argv)>1:
                        debug()
                    else:
                        b.quit()
                        exit("Something went wrong... run in debugging mode to see what!")

            elif ch=='3':
                if pause==0:
                    pause = 1
                    b.find_element_by_class_name('play-song').click()
                    print("\nPlayback PAUSED\n")
                else:
                    pause = 0
                    b.find_element_by_class_name('play-song').click()
                    print("\nResuming Playback\n")

            elif ch=='4':
                try:
                    b.find_element_by_class_name('prev-song').click()
                    print("\nPlaying the last song....\n")
                except:
                    debug()

            elif ch=='5':
                print(("\nTrack name : "+b.find_element_by_id('stitle').text+' from the album -  '+b.find_element_by_id('atitle').text+'\n'))
                print(("Track time : "+b.find_element_by_class_name('timer-wrap').text+'\n'))

            elif ch=='6':
                print('\nStopping current playback...\n')
                b.get('https://gaana.com/playlist/gaana-dj-international-weekly-hot-20')
                time.sleep(3)
                b.find_element_by_id('p-list-play_all').click()

            elif ch=='7':
                if rep==0:
                    rep=1
                    b.find_element_by_class_name('repeat').click()
                    print('\nRepeat mode ON\n')
                elif rep==1:
                    rep=0
                    for i in range(0,2):
                        b.find_element_by_class_name('repeat').click()
                    print('\nRepeat mode OFF\n')

            elif ch=='8':
                debug()
            elif ch=='exit':
                b.quit()
                sys.exit('Stopping playback...Closing Saavn...')
            else:
                print('wrong choice!\n')
                pass

    except selenium.common.exceptions.ElementClickInterceptedException:
        print('\nPlease select again... Sorry for minor inconvenience\n')
        b.find_element_by_tag_name('html').send_keys(Keys.ESCAPE)
        handler()

def navigate(artist):
    try:
        b.get('http://gaana.com/search/{}'.format(artist))
    except:
        b.quit()
        sys.exit('\nCheck your internet connection and try again...\n')

    #logic to start playback, selects first result:

    try:
        time.sleep(5)
        b.execute_script("arguments[0].click();",b.find_element_by_class_name('imghover'))
        time.sleep(3)
        b.find_element_by_id('p-list-play_all').click()
    except:
        if len(sys.argv)>1:
            debug()
        else:
            b.quit()
            exit("Something went wrong... run in debugging mode to see what!")

    handler()

navigate(artist)
