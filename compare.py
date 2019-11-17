#!/usr/bin/python3
import requests,sys,webbrowser,re,random
from threading import Thread
from bs4 import *

COLLECTIONS = dict()

def get_source(url):
    try:
        USER_AGENTS = [
        ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/57.0.2987.110 '
        'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/61.0.3163.79 '
        'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
        'Gecko/20100101 '
        'Firefox/55.0'),  # firefox
        ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/61.0.3163.91 '
        'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/62.0.3202.89 '
        'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/63.0.3239.108 '
        'Safari/537.36'),  # chrome
        ]
        headers = {'User-Agent':random.choice(USER_AGENTS)}
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

def amazon(search_term):
    global COLLECTIONS
    base_url = "https://www.amazon.in"
    source = get_source(base_url+"/s?k={}".format(search_term))
    if 'captcha' in source.lower():
        exit("fucked")
    s = BeautifulSoup(source,'html.parser')

    names = []
    prices = []
    links = []

    items = s.findAll('div',attrs={'data-index':re.compile(r'\d+')})
    for item in items:
        try:
            price = item.find('span',attrs={'class':'a-price','data-a-size':'l','data-a-color':'price'})
            prices.append('₹'+price.text.split('₹')[1])
            names.append(item.select_one('h2 > a > span').text)
            links.append(base_url+item.find('a',attrs={'class':'a-link-normal a-text-normal'}).get('href'))
        except AttributeError:
            pass
    #print(len(names),len(prices),len(links))
    COLLECTIONS[1] = dict(zip(names,zip(prices,links)))

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
    COLLECTIONS[2] = dict(zip(names,zip(prices,links)))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        search_term = '+'.join(input("Enter the item you would like to compare...\n> ").split())
    else:
        search_term = '+'.join(sys.argv[1:])

    t1 = Thread(target=amazon,args=(search_term,))
    t1.start()
    t2 = Thread(target=flipkart,args=(search_term,))
    t2.start()

    try:
        while True:
            service = int(input("\nChoose :\n1. AMAZON RESULTS\n2. FLIPKART RESULTS\n3. EXIT\n>  "))
            if service not in [1,2,3]:
                print("Wrong choice! bye!")
                pass
            if service == 3:
                raise KeyboardInterrupt
            if t1.isAlive() or t2.isAlive():
                t1.join()
                t2.join()

            for index,item in enumerate(COLLECTIONS[service].keys(),1):
                print("\n{0} - \u001b[33m{1}\033[m COSTS \u001b[31m{2}\033[m.\nLINK : \033[0;34m{3}\033[m.".format(index,item,COLLECTIONS[service][item][0],COLLECTIONS[service][item][1]))

            ch = input("\nEnter the number to open link...\n> ")

            try:
                for index,item in enumerate(COLLECTIONS[service].keys(),1):
                    if ch == str(index):
                        webbrowser.open(COLLECTIONS[service][item][1])
            except:
                pass
    except KeyboardInterrupt:
        exit('bye!')
    except:
        print("Oops... Something's fishy")
