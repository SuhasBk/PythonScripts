#!/usr/bin/python3
from bs4 import *
import random

common = open("/Users/gandalf/Downloads/Vocab/Common.html").read()
advanced = open("/Users/gandalf/Downloads/Vocab/Advanced.html").read()
combined = common + advanced

s = BeautifulSoup(combined, 'html.parser')
pairs = s.findAll("tr")
visited = set()

while True:
    card = random.choice(pairs)
    td = card.findAll("td")
    word = td[0].text.upper()
    if word not in visited:
        visited.add(word)
        print("\nWORD - ", word)
        input("\nShow Meaning?")
        print("\nMEANING - ", td[1].text)
