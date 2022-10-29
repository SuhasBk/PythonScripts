#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import sys

word = None

if len(sys.argv) > 1:
    word = sys.argv[1]

while True:
    if not word:
        word = input("\n\nEnter the word\n")

    try:
        r = requests.get("https://www.wordnik.com/words/{}".format(word), headers={'User-Agent': 'masterbyte'})
        s = BeautifulSoup(r.text, 'html.parser')
        print(s.find("div", {'id': 'define'}).text)
        
        # meanings = s.findAll('p')
        # for index, meaning in enumerate(meanings, 1):
        #     print(index, ' - ', meaning.text.strip())
    except:
        print('No such word in my dictionary...')
    word = None
