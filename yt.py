#!/usr/bin/python3
import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from open_apps import start

if len(sys.argv[1:])==0:
    search_term = ' '.join(input("Enter the search term\n").split())
else:
    search_term = ' '.join(sys.argv[1:])

print("Searching... Please wait...")

try:
    session = requests.Session()
    headers = {'User-Agent': 'masterbyte'}
    session.headers.update(headers)
    r = session.get("http://youtube.com/results?search_query=" + '+'.join(search_term.split()))
except requests.HTTPError as err:
    print(err)
    exit()

s = BeautifulSoup(r.text, 'html.parser')

data = str(s.findAll('script')[26])
bundle = re.findall(r'accessibilityData\":\{\"label\":\"(.{10,200}) views\"\}\}\}',data)

video_ids = re.findall(r'\"/watch\?v=(.{11})\"', data)
urls = list(map(lambda id : "http://youtube.com/watch?v="+id,video_ids))

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
    video_choice = input("Enter the number corresponding to the link (type 'exit' to quit)- \n")

    if video_choice == 'exit':
        sys.exit('Ciao!')
    
    video_choice = int(video_choice)

    if video_choice >= len(urls):
        print('\nWrong Input!\n')
    else:
        url = urls[video_choice]
        title = titles[video_choice]

        print(f"\nTitle of video : {title}\nYouTube video URL : {url}")

        download = True if input("\nDo you wish to stream the video (type 'v', requires VLC) or download (type 'd', requires youtube-dl) it?\n").lower().startswith('d') else False

        if download:
            audio_only = True if input("\nDo you wish to download the audio (type 'a') or video (type 'v')?\n").lower().startswith('a') else False

            if audio_only:
                print("\nDownloading audio in .webm format by default... if ffmpeg is installed, file will be converted to .mp3 format")
                start("youtube-dl", "--extract-audio", "--audio-format", "mp3", url)
            else:
                print("\nDownloading video as mp4...")
                start("youtube-dl", url)   
        else:
            print("Streaming via VLC...")
            start('vlc', url)
                
