#!/usr/local/bin/python3
import sys
import requests
from bs4 import BeautifulSoup

session = requests.Session()

# goto download page:
response = session.get("https://ubuntu.com/download/desktop")
soup = BeautifulSoup(response.text, 'html.parser')

# get latest stable version link always:
download_page_url = "https://ubuntu.com" + soup.select('a.p-button--positive.is-wide')[0].get('href')
response = session.get(download_page_url)

# get ISO download url:
soup = BeautifulSoup(response.text, 'html.parser')
iso_download_url = soup.select('p > a[href]')[1].get('href')

# download iso:
file_name = "ubuntu.iso"
with open(file_name, "wb") as f:
    print("Downloading %s" % file_name)
    
    # 'stream = True' => download response headers, but defer downloading content and keep the connection alive:
    response = requests.get(iso_download_url, stream = True)
    total_length = response.headers.get('content-length')

    # no content length header:
    if total_length is None:
        f.write(response.content)
    else:
        dl = 0
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            f.write(data)
            done = int(50 * dl / total_length)
            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
            sys.stdout.flush()
