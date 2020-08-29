#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from fake_useragent import  UserAgent
import sys

if len(sys.argv) > 1:
    word = sys.argv[1]
else:
    word = input("Enter the word\n")

try:
    r = requests.get("https://dictionary.cambridge.org/dictionary/english/{}".format(word), headers={'User-Agent': 'masterbyte'})
    s = BeautifulSoup(r.text,'html.parser')
    sections = s.findAll('div',attrs={'class':'sense-body'})
    meaning = ''
    for i in sections:
        meaning += i.text
    if len(meaning) == 0:
        raise AttributeError
    print("Word : '{}'\n\nMeaning : {}".format(word,meaning.lstrip()))
except AttributeError:
    print('No such word in my dictionary...')
