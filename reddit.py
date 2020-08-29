#!/usr/local/bin/python3
import requests
import os,time,sys
from getpass import getpass
from subprocess import run,PIPE

sess = []

def login():
    global sess
    username = os.environ.get('REDDIT_UNAME', input("Enter your reddit username\n"))
    passwd = os.environ.get('REDDIT_PWD', getpass("Enter the password (hidden)\n"))
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

if __name__ == '__main__':
    login()
    html = ''
    sub = input("Enter a VALID subreddit\n> ")
    results(sub)
