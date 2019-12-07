#!/usr/bin/python3
from subprocess import *
import os,sys

if sys.platform=='linux':
    DIR = '/mnt/Universe/tv_movies/series'
else:
    DIR = r'E:\tv_movies\series'

series_list = os.listdir(DIR)
for i,j in enumerate(series_list[:]):
    print(i,' : ',j)
sh = int(input("Enter the choice:\n> "))

for i,j in enumerate(series_list):
    if sh==i:
        season_list = os.listdir(os.path.join(DIR,j))
        for p,q in enumerate(season_list[:]):
            print(p,' : ',q)
        se = int(input("Enter the choice:\n> "))

        for k,l in enumerate(season_list[:]):
            if se==k:
                episode_list = list(filter(lambda x : '.mkv' in x or '.mp4' in x,os.listdir(os.path.join(DIR,j,l))))
                e = os.path.join(DIR,j,l,episode_list[0])
                Popen(["vlc",e],stdout=PIPE,stderr=PIPE)
