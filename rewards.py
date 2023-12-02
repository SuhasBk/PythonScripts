#!/usr/local/bin/python3
from subprocess import run
import webbrowser
import random
import requests
from nltk.corpus import words
import sys, time
import pyautogui as gui
from itertools import permutations

def mobile():
    forms = [''.join(i) for i in permutations('WTFIG')]
    for i in range(26):
        item = random.choice(items)
        if item not in s:
            url = f"https://www.bing.com/search?q={item}\\&form=" + random.choice(forms)
            run(['adb', 'shell', 'am', 'start', '-n', EDGE_ACTIVITY, '-d', url])
            time.sleep(random.randint(5, 40) * 0.1)
        else:
            i -= 1
        s.add(item)

def desktop():
    forms = [''.join(i) for i in permutations('DSKTP')]
    i = 0
    while i<31:
        item = random.choice(items)
        if item not in s:
            url = f"https://www.bing.com/search?q={item}&form=" + random.choice(forms)
            webbrowser.open(url)
            time.sleep(random.randint(5, 20) * 0.1)
            i += 1
        s.add(item)
    
    time.sleep(3)

    for i in range(31):
        gui.hotkey('command', 'w')
        time.sleep(0.5)

def mobile_new():
    i = 0
    while i<26:
        item = random.choice(items)
        if item not in s:
            if i==0:
                # start browser
                url = f"https://www.bing.com/search?q={item}\\&form=WTFIG"
                run(['adb', 'shell', 'am', 'start', '-n', EDGE_ACTIVITY, '-d', url])
                time.sleep(4)
            else:
                # search bar
                run(['adb', 'shell', 'input', 'tap', '500', '100'])
                time.sleep(0.2)
                # clear text
                run(['adb', 'shell', 'input', 'tap', '1000', '100'])
                # search word
                run(['adb', 'shell', 'input', 'text', item])
                # press enter
                run(['adb', 'shell', 'input', 'keyevent', '66'])
                time.sleep(random.randint(3, 7))
            i += 1
        s.add(item)

def desktop_new():
    i = 0
    while i<32:
        item = random.choice(items)
        if item not in s:
            if i==0:
                url = f"https://www.bing.com/search?q={item}&form=DSKTP"
                webbrowser.open(url)
            else:
                gui.hotkey('command', 't')
                gui.write(item)
                time.sleep(1)
                gui.press('enter')
            time.sleep(random.randint(3, 7))
            i += 1
        s.add(item)
    
    time.sleep(3)
    for i in range(31):
        gui.hotkey('command', 'w')
        time.sleep(0.5)

if __name__ == '__main__':
    EDGE_ACTIVITY = "com.microsoft.emmx/com.microsoft.ruby.Main"
    s = set()

    try:
        r = requests.get('https://random-word-api.herokuapp.com/word?number=100')
        items = r.json()
    except:
        items = random.sample(words.words(), 100)    

    try:
        webbrowser.open("https://rewards.bing.com/pointsbreakdown")
        arg1 = sys.argv[1]
        if arg1 == 'mobile':
            mobile_new()
        else:
            desktop_new()
    except IndexError:
        mobile_new()
        desktop_new()
