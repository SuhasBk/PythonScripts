#!/usr/bin/python3
import requests,sys,webbrowser,re,random
from threading import Thread
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

COLLECTIONS = dict()
ua = UserAgent()

def get_source(url):
    try:
        headers = {'User-Agent':ua.random}
        r = requests.get(url,headers=headers)
        if r.ok:
            return r.text
        else:
            print(r.url)
            exit(str(r.status_code))
    except requests.exceptions.ConnectionError:
        exit("Please check your internet connection and try again...")
    except:
        exit("Something went wrong while handling requests... Contact administrator...")

def flipkart(search_term):
    global COLLECTIONS
    base_url = "http://www.flipkart.com"
    source = get_source(base_url+"/search?q={}".format(search_term))
    s = BeautifulSoup(source,'html.parser')

    names = []
    prices = []
    links = []

    items = s.findAll('div',attrs={'class':'_1UoZlX'})
    if len(items) != 0:
        for item in items:
            prices.append(item.find('div',attrs={'class':'_1vC4OE _2rQ-NK'}).text)
            names.append(item.find('div',attrs={'class':'_3wU53n'}).text)
            links.append(base_url+item.find('a',attrs={'class':'_31qSD5'}).get('href'))
    else:
        items = s.findAll('div',attrs={'class':'_3O0U0u'})
        for item in items:
            prices.append(item.find('div',attrs={'class':'_1vC4OE'}).text)
            names.append(item.find('a',attrs={'class':'_2cLu-l'}).text+' '+item.find('div',attrs={'class':'_1rcHFq'}).text)
            links.append(base_url+item.find('a',attrs={'class':'Zhf2z-'}).get('href'))

    #print(len(names),len(prices),len(links))
    COLLECTIONS[0] = dict(zip(names,zip(prices,links)))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        search_term = '+'.join(input("Enter the item you would like to compare...\n> ").split())
    else:
        search_term = '+'.join(sys.argv[1:])

    t = Thread(target=flipkart,args=(search_term,))
    t.start()

    if t.is_alive():
        t.join()

    try:
        for index,item in enumerate(COLLECTIONS[0].keys(),1):
            print("\n{0} - \u001b[33m{1}\033[m COSTS \u001b[31m{2}\033[m.\nLINK : \033[0;34m{3}\033[m.".format(index,item,COLLECTIONS[0][item][0],COLLECTIONS[0][item][1]))

        ch = input("\nEnter the number to open link...\n> ")

        try:
            for index,item in enumerate(COLLECTIONS[0].keys(),1):
                if ch == str(index):
                    webbrowser.open(COLLECTIONS[0][item][1])
        except:
            pass
    except KeyboardInterrupt:
        exit('bye!')
