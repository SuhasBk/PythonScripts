#!/usr/bin/python3
import requests
import re,sys
from bs4 import *

def lyrics(song_name):
    r = requests.get("https://search.azlyrics.com/search.php?q="+'+'.join(song_name.split()),headers={'User-Agent':'MyApp'})
    s = BeautifulSoup(r.text,'html.parser')
    td = s.findAll('td',attrs={'class':'text-left visitedlyr'})
    res = []

    if len(td) == 0:
        custom = input("No results found for this...Want to try again? (y)\n")
        if custom =='y':
            lyrics()
        else:
            print('\nOkay... returning to main menu...\n')
        return

    for i,j in enumerate(td):
        s=re.findall(r'<b>.*</b>',str(j))[0]
        for r in (('<b>',''),('</b>',''),('</a>','')):
            s=s.replace(*r)
        print(i,s)
        res.append(j.find('a').get('href'))

    choice = input("\nChoose one from above : (type 'exit' to quit)\n")

    for i,j in enumerate(res):
        if choice==str(i):
            q = requests.get(j,headers={'user-agent':'MyApp'})
            s = BeautifulSoup(q.text,'html.parser')
            l = s.find('div',attrs={'class':'col-xs-12 col-lg-8 text-center'})
            try:
                print(l.find('div',attrs={'class':''}).text)
            except AttributeError:
                print('\nOops! Requested lyrics not available...\n')
        elif choice == 'exit':
            return

if __name__ == '__main__':
    try:
        song_name = ' '.join(sys.argv[1:])
    except:
        song_name = input("Enter the name of the song\n> ")

    lyrics(song_name)
