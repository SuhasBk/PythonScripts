#!/usr/local/bin/python3
import os
from getpass import getpass
from subprocess import PIPE, run

import requests

sess = []

def login():
    global sess
    username = os.environ.get('REDDIT_UNAME', "")
    passwd = os.environ.get('REDDIT_PWD', "")
    user = {'user':username,'passwd':passwd,'api_type':'json'}
    s = requests.Session()
    headers = {'User-Agent': 'masterbyte'}
    s.headers.update(headers)
    s.post('https://reddit.com/api/login',data=user)
    sess.append(s)

def results(sub):
    global sess, html
    html = sess[0].get('https://reddit.com/r/{}/.json?limit=50'.format(sub)).json()

    for i in range(50):
        data = html['data']['children'][i]['data']
        print(i, ':', data['title'].upper(), '-', data['url'])

    if os.uname().sysname.startswith("Darwin"):
        counter = 0
        while True:
            user_ch = input("\nEnter your choice:\n> ")

            if user_ch != "":
                ch = int(user_ch)
                print(ch, end=' - ')
                url = str(html['data']['children'][ch]['data']['url'])
                title = html['data']['children'][ch]['data']['title']
                counter = ch + 1
            else:
                print(counter, end=' - ')
                url = str(html['data']['children'][counter]['data']['url'])
                title = html['data']['children'][counter]['data']['title']
                counter += 1

            print(title)
            run('open -na "Google Chrome" --args --incognito ' + url, shell=True)

if __name__ == '__main__':
    login()
    html = ''
    sub = input("Enter a VALID subreddit\n> ")
    results(sub)
