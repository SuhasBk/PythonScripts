#!/usr/bin/python3
import os,sys,time
from subprocess import *

def list_songs():
    global directory,songs
    a = input("\nTell me child, what do you seek in your music directoryectory?\n")
    print("SONG ID - SONG NAME")
    for i,j in enumerate(songs):
        if a == 'exit':
            raise KeyboardInterrupt
        if a.lower() in j.lower():
            print(str(i)+' - '+j)
    choice = input("\nEnter the song number to add to your playlist...\nEnter 'exit' to quit:\n> ")
    add_to_playlist(choice)

def add_to_playlist(choice):
    global playlist,directory,songs
    for q,p in enumerate(songs):
        if(choice==str(q)):
            playlist.add(os.path.join(directory,p))
            print("\nAdded '{}' to playlist...".format(p))

            print(f"Current playlist size : {len(playlist)}\nCurrent playlist songs : {playlist}")

            confirm = input("\nWhat do you want to do?\n\n1) Start playing current playlist\n2) Add more songs to playlist with the song ID\n3) Search the library again\n\nEnter 'exit' to quit\n> ")

            if confirm == '1':
                for song in range(len(playlist)):
                    Popen(["vlc","--playlist-enqueue","-L",playlist.pop()],close_fds=True,stdout=PIPE,stderr=PIPE)

            elif confirm == '2':
                ch = input("\nEnter the song number to add to your playlist...\n\nEnter 'exit' to quit:\n> ")
                if ch == 'exit':
                    raise KeyboardInterrupt
                add_to_playlist(ch)

            elif confirm == '3':
                list_songs()

            elif confirm == 'exit':
                raise KeyboardInterrupt

def handler():
    while True:
        try:
            list_songs()
        except KeyboardInterrupt:
            exit('bye')

if __name__ == '__main__':
    if sys.platform == 'linux':
        directory = '/mnt/Universe/music/'
    elif 'win' in sys.platform.lower():
        directory = 'E:\\music'

    songs = os.listdir(directory)
    playlist = set()

    handler()
