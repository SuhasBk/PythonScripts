#!/usr/local/bin/python3

# BIG GUN:

# import os
# import sys
# import time
# from msedge.selenium_tools import Edge, EdgeOptions

# opt = EdgeOptions()
# opt.use_chromium = True
# del opt.capabilities['platform']
# if len(sys.argv[1:]) == 0:
#     opt.add_argument('--headless')

# browser = Edge(options=opt, service_log_path=os.path.devnull)
# browser.maximize_window()
# browser.get('https://epaper.hindustantimes.com/Home/ArticleView')

# browser.execute_script(f'DownloadAsEditionPdf("102","{date.day}/{str(date.month).zfill(2)}/{date.year}",5)')
# time.sleep(5)
# browser.quit()

# much elegant:

import sys
import os
import requests
import shutil
from datetime import date

date = date.today()
file_name = str(date)+'.pdf'
session = requests.Session()

file_download_url = f"https://epaper.hindustantimes.com/Home/Download?id=102&type=5&EditionId=102&Date={str(date.day).zfill(2)}%2F{str(date.month).zfill(2)}%2F{date.year}"

with session.get(file_download_url, stream=True) as r:
    with open(file_name, 'wb+') as f:
        shutil.copyfileobj(r.raw, f, length=16*1024*1024)

session.close()

if sys.platform == 'darwin':
    os.system(f"open {file_name}")
elif sys.platform.startswith('linux'):
    os.system(f"xdg-open {file_name}")
else:
    os.startfile(file_name)
