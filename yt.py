#!/usr/bin/python3
import re,os,sys
from subprocess import PIPE,run,Popen
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

if len(sys.argv[1:])==0:
    search_term = ' '.join(input("Enter the search term\n").split())
else:
    search_term = ' '.join(sys.argv[1:])

print("Searching... Please wait...")

try:
    session = requests.Session()
    headers = {'User-Agent': UserAgent().random}
    session.headers.update(headers)
    r = session.get("http://youtube.com/results?search_query=" + '+'.join(search_term.split()))
except requests.HTTPError as err:
    print(err)
    exit()

s = BeautifulSoup(r.text, 'html.parser')

data = str(s.findAll('script')[26])
bundle = re.findall(r'accessibilityData\":\{\"label\":\"(.{10,200}) views\"\}\}\}',data)

video_ids = re.findall(r'\"/watch\?v=(.{11})\"', data)
urls = list(map(lambda id : "https://youtube.com/watch?v="+id,video_ids))

titles = [re.findall(r'(.*) by', i)[0] for i in bundle]
uploaded = [re.findall(r'by .* (.* .*) ago', i)[0] for i in bundle]
durations = [re.findall(r'ago (.*) .*', i)[0] for i in bundle]
views = [re.findall(r'ago .* (.*)', i)[0] for i in bundle]
uploaders = [re.findall(r'by (.*) .* .* ago', i)[0] for i in bundle]

for i,t,up,d,v,ur,us in zip(range(5),titles,uploaded,durations,views,urls,uploaders):
    p = session.get(ur)
    q = BeautifulSoup(p.text,'html.parser')
    try:
        likes = re.findall(r'{\"accessibilityData\":\{\"label\":\"([0-9]+(,[0-9]+)*) likes',str(q))[0][0]
        dislikes = re.findall(r'{\"accessibilityData\":\{\"label\":\"([0-9]+(,[0-9]+)*) dislikes',str(q))[0][0]
    except IndexError:
        likes = 'NA'
        dislikes = 'NA'
    print('<<< ',str(i),' >>> : ',t,'\nYouTube URL\t:\t',ur,'\nUPLOADED\t:\t',up,'\nDURATION\t:\t',d,'\nVIEWS\t\t:\t',v,'\nLIKES\t\t:\t',likes,'\nDISLIKES\t:\t',dislikes,'\nUPLOADER\t:\t',us,'\n')


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
                    Popen(['vlc',j],stderr=PIPE,stdout=PIPE)
                except FileNotFoundError:
                    Popen([input("Enter your default media player...\nEx: 'mpv','totem','vlc' : "),j],stderr=PIPE,stdout=PIPE,close_fds=True)
