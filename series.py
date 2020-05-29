#!/usr/bin/python3
from subprocess import Popen,PIPE
import os,sys

if sys.platform=='linux':
    ROOT_DIR = '/mnt/Universe/tv_movies/series'
else:
    ROOT_DIR = r'E:\tv_movies\series'
    
series_list = list(map( lambda x : os.path.join(ROOT_DIR,x),os.listdir(ROOT_DIR)))
series_list = list(filter(lambda x : os.path.isdir(x),series_list))

for i,j in enumerate(series_list):
    print(i,' : ',j[j.rfind(os.path.sep)+1:])

ch = int(input("Enter the choice:\n> "))

series = os.path.join(ROOT_DIR, series_list[ch])

season_list = os.listdir(series)
for p,q in enumerate(season_list):
    print(p,' : ',q)

ch = int(input("Enter the choice:\n> "))

season = os.path.join(series,season_list[ch])

if os.path.isdir(season):
    episode_list = os.listdir(season)
    episode_list = list(filter(lambda x : '.srt' not in x and '.txt' not in x,episode_list))
    
    for z,w in enumerate(episode_list):
        print(z,' : ',w)
    
    ch = int(input("Enter the choice:\n> "))

    episode = os.path.join(season,episode_list[ch])
    
    if os.path.isdir(episode):
        fname = list ( filter ( lambda x : '.srt' not in x and '.txt' not in x, os.listdir(episode) ) )
        Popen(["vlc",fname[0]],stdout=PIPE,stderr=PIPE)
    else:
        Popen(["vlc",episode],stdout=PIPE,stderr=PIPE)

elif os.path.isfile(season):
    Popen(["vlc",season],stdout=PIPE,stderr=PIPE)
