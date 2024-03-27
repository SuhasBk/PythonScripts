#!/usr/bin/python3
import requests, sys
from bs4 import BeautifulSoup

if len(sys.argv) < 3:
    exit('Please pass the episode number as argument')
else:
    show = sys.argv[1]
    ep_check = int(sys.argv[2])

r = requests.get(f"https://www.animefillerlist.com/shows/{show}")

s = BeautifulSoup(r.text, 'html.parser')

tr_filler = s.findAll('tr', {'class': 'filler'})

filler_ep_list = list(map(lambda x: int(x.td.text), tr_filler))

if len(sys.argv) > 2:
    print(filler_ep_list)

if ep_check in filler_ep_list:
    while ep_check in filler_ep_list:
        ep_check += 1
    print(f'\nSkip it!!! Go to - {ep_check}\n')
else:
    while ep_check not in filler_ep_list:
        ep_check += 1
    print(f'\nNope... Next filler at - {ep_check}\n')