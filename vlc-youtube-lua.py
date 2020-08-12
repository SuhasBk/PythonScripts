#!/usr/bin/python3
import requests
import os
import sys
import struct
import shutil

SOURCE_URL = 'https://raw.githubusercontent.com/videolan/vlc/master/share/lua/playlist/youtube.lua'
LOCATIONS = {
    'win': {
        32: r'C:\\Program Files\\VideoLAN\\VLC\\lua\\playlist',
        64: r'C:\\Program Files (x86)\\VideoLAN\\VLC\\lua\\playlist'
    },
    'linux': {
        32: '/usr/lib/vlc/lua/playlist/',
        64: '/usr/lib64/vlc/lua/playlist/'
    },
    'mac': {
        64: '/Applications/VLC.app/Contents/MacOS/share/lua/playlist/'
    }
}

this_os = 'win' if sys.platform.startswith('win') else 'mac' if sys.platform.startswith('darwin') else 'linux'
this_os_architecture = struct.calcsize("P") * 8

target = LOCATIONS[this_os][this_os_architecture]
file_name = 'youtube.lua'

session = requests.Session()
session.headers.update({'User-Agent': 'VLC is the best!'})
r = session.get(SOURCE_URL)
session.close()

if r.ok:
    open(file_name, 'wb+').write(r.content)
    src = os.path.join(os.getcwd(), file_name)
    dest = os.path.join(target, file_name)
    
    shutil.move(file_name, dest)
    print("Hacked! You can now stream YouTube videos on VLC!")
else:
    print(f"Check your internet connection...\nError:{r.status_code}")