#!/usr/bin/python3
import re
import sys
import requests
from bs4 import BeautifulSoup
from open_apps import start

session = requests.Session()
headers = {'User-Agent': 'masterbyte'}
session.headers.update(headers)

def fetch():
    if len(sys.argv[1:])==0:
        query = input("Enter the search term\n")
        search_term = ' '.join(query.split())
    else:
        query = ' '.join(sys.argv[1:])
        search_term = query

    print(f"\nSearching for {query}... Please wait...\n")

    try:
        r = session.get("http://youtube.com/results?search_query=" + '+'.join(search_term.split()))
    except requests.HTTPError as err:
        print(err)
        exit()

    urls = re.findall('{"videoId":"(\w+)"', r.text)
    urls = list(map(lambda x: 'https://youtube.com/watch?v='+x, (sorted(set(urls), key=urls.index))))
    return urls

def watch(urls):
    for i,ur in zip(range(5),urls):
        p = session.get(ur)
        q = BeautifulSoup(p.text,'html.parser')
        t = q.find('title').text
        print('<<< ',str(i),' >>> : ',t,'\nYouTube URL\t:\t',ur)


    while True:
        video_choice = input("Enter the number corresponding to the link (type 'exit' to quit)- \n")

        if video_choice == 'exit':
            sys.exit('Ciao!')
        
        video_choice = int(video_choice)

        if video_choice >= len(urls):
            print('\nWrong Input!\n')
        else:
            url = urls[video_choice]

            download = True if input("\nDo you wish to stream the video (type 'v', requires VLC) or download (type 'd', requires youtube-dl) it?\n").lower().startswith('d') else False

            if download:
                audio_only = True if input("\nDo you wish to download the audio (type 'a') or video (type 'v')?\n").lower().startswith('a') else False

                if audio_only:
                    print("\nDownloading audio in .webm format by default... if ffmpeg is installed, file will be converted to .mp3 format")
                    start("youtube-dl", "--no-check-certificate", "--extract-audio", "--audio-format", "mp3", url)
                else:
                    print("\nDownloading video as mp4...")
                    start("youtube-dl", url)

                break   
            else:
                print("Streaming via VLC...")
                start('vlc', url)
                
if __name__ == '__main__':
    urls = fetch()
    watch(urls)
