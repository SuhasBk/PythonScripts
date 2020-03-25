#!/usr/bin/python3
import requests
import os,time,sys
from getpass import getpass
from threading import Thread
from subprocess import run,PIPE
from fake_useragent import UserAgent

sess = []

def login():
    global sess
    username = input("Enter your reddit username\n")
    passwd = getpass("Enter the password (hidden)\n")
    user = {'user':username,'passwd':passwd,'api_type':'json'}
    s = requests.Session()
    s.headers.update({'User-Agent':UserAgent().random})
    s.post('https://reddit.com/api/login',data=user)
    sess.append(s)

def results(sub):
    global sess
    html = sess[0].get('https://reddit.com/r/{}/.json?limit=50'.format(sub)).json()

    res = []

    for i in range(50):
        if html['data']['children'][i]['data']['media']:
            try:
                print(i,html['data']['children'][i]['data']['title'])
                res.append([i,html['data']['children'][i]['data']['preview']['reddit_video_preview']['fallback_url']])
            except:
                pass

    while True:
        try:
            ch = input("Enter the choice ('-1' for new sub)\n")
            for i,j in res:
                if ch == str(i):
                    if 'win' in sys.platform.lower():
                        run(["vlc","--fullscreen",j],stdout=PIPE,stderr=PIPE,close_fds=True)
                    else:
                        run(["vlc","--fullscreen","--loop",j],stdout=PIPE,stderr=PIPE,close_fds=True)
                elif ch == '-1':
                    results(input("Enter the new subreddit\n> "))
                elif ch == 'exit':
                    raise KeyboardInterrupt
        except KeyboardInterrupt:
            exit('bye')

if __name__ == '__main__':
    t = Thread(target=login)
    t.start()
    sub = input("Enter a VALID subreddit\n> ")
    t.join()
    results(sub)
