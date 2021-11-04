#!/usr/local/bin/python3
from open_apps import start
import os,sys

if sys.platform=='linux':
    ROOT_DIR = '/mnt/Universe/tv_movies/series'
elif sys.platform == 'darwin':
    ROOT_DIR = '/Users/gandalf/Movies/TV'
else:
    ROOT_DIR = r'E:\tv_movies\series'

file_filter = lambda x: '.srt' not in x and '.txt' not in x and '.unwanted' not in x and '.parts' not in x
    
series_list = list(map( lambda x : os.path.join(ROOT_DIR,x),os.listdir(ROOT_DIR)))
series_list = sorted(list(filter(lambda x : os.path.isdir(x),series_list)))

for i,j in enumerate(series_list,1):
    print(i,' : ',j[j.rfind(os.path.sep)+1:])

ch = int(input("Enter the choice:\n> ")) - 1

series = os.path.join(ROOT_DIR, series_list[ch])

season_list = sorted(os.listdir(series))
season_list = list(filter(file_filter, season_list))

for p,q in enumerate(season_list,1):
    print(p,' : ',q)

ch = int(input("Enter the choice:\n> ")) - 1

season = os.path.join(series,season_list[ch])

if os.path.isdir(season):
    episode_list = sorted(os.listdir(season))
    episode_list = list(filter(file_filter, episode_list))
    
    for z,w in enumerate(episode_list,1):
        print(z,' : ',w)
    
    while True:
        ch = int(input("Enter the choice:\n> ")) - 1

        episode = os.path.join(season,episode_list[ch])
        
        if os.path.isdir(episode):
            fname = list ( filter ( file_filter, sorted(os.listdir(episode)) ) )
            start("vlc", fname[0])
        else:
            start("vlc", episode)

elif os.path.isfile(season):
    start("vlc", season)
