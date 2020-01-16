#!/usr/bin/python3
import re,os,sys
from subprocess import PIPE,run,Popen
import requests
from bs4 import BeautifulSoup

if len(sys.argv[1:])==0:
    search_term = ' '.join(input("Enter the search term\n").split())
else:
    search_term = ' '.join(sys.argv[1:])

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'}

try:
    r = requests.get("http://youtube.com/results?search_query=" + '+'.join(search_term.split()))
except requests.HTTPError as err:
    print(err)
    exit()

print("Searching....")
s = BeautifulSoup(r.text, 'html.parser')
l = s.findAll('a',{'class':'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link','rel':'spf-prefetch'})

urls = []
titles = []
durations = []
uploaded = []
views = []
uploaders = []

for i in l:
    urls.append('http://youtube.com'+i.get('href'))
    titles.append(i.text)
    durations.append(re.findall('\w+:\w+',i.parent.text)[0])
    meta = i.parent.parent.find('ul',{'class':'yt-lockup-meta-info'}).findAll('li')
    uploaded.append(meta[0].text)
    views.append(meta[1].text)
    uploaders.append(i.parent.parent.find('div',{'class':"yt-lockup-byline"}).text)

for i,t,up,d,v,ur,us in zip(range(5),titles,uploaded,durations,views,urls,uploaders):
    p = requests.get(ur)
    q = BeautifulSoup(p.text,'html.parser')
    likes = q.find('button',{'title':'I like this'}).text
    dislikes = q.find('button',{'title':'I dislike this'}).text
    print('<<< '+str(i)+' >>> : '+t+'\nYouTube URL\t:\t'+ur+'\nUPLOADED\t:\t'+up+'\nDURATION\t:\t'+d+'\nVIEWS\t\t:\t'+v+'\nLIKES\t\t:\t'+likes+'\nDISLIKES\t:\t'+dislikes+'\nUPLOADER\t:\t'+us+'\n')


while True:
    ch=input("Enter the number corresponding to the link (type 'exit' to quit)- \n")
    if ch=='exit':
        exit('Bye')
    for i,j in enumerate(urls):
        if ch==str(i):
            print(j)
            dorv=input("Ok! So, do you want to stream the video (type 'v') or download (type 'd', requires youtube-dl) it?\n")
            if dorv == 'd':
                mp3=input("Do you want to download the audio (type 'a') or video (type 'v')?\n")
                if mp3 == 'v':
                    print("Downloading video...")
                    run(["youtube-dl",j],shell=True)
                else:
                    print("Downloading audio...")
                    run(["youtube-dl", "--extract-audio", "--audio-format","mp3",j])
            elif dorv == 'v':
                print("Streaming...")
                try:
                    Popen(['vlc',j],close_fds=True,stderr=PIPE,stdout=PIPE)
                except FileNotFoundError:
                    Popen([input("Enter your default media player...\nEx: 'mpv','totem','vlc' : "),j],stderr=PIPE,stdout=PIPE,close_fds=True)
