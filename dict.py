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
        r = requests.get("https://www.lexico.com/definition/{}".format(word), headers={'User-Agent': 'masterbyte'})
        s = BeautifulSoup(r.text, 'html.parser')
        
        meanings = s.findAll('span',{'class':'ind'})
        for index, meaning in enumerate(meanings, 1):
            print(index, ' - ', meaning.text)
    except:
        print('No such word in my dictionary...')
    word = None
