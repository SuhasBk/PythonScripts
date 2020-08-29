#!/usr/local/bin/python3
import requests
import sys

try:
    url = sys.argv[1]
    fname = sys.argv[2]
except:
    url = input("Enter the HTTP URL of a file:\n> ")
    fname = input("Enter the file name/path without extension:\n> ")

pos = url.rfind('.')
if pos!=-1:
    ext = url[url.rfind('.'):]
    fname+=ext
else:
    exit("URL should point to a specific file on the internet...Please check and try again...")

r = requests.get(url)
if r.ok:
    open(fname,'wb+').write(r.content)
    exit(f"File saved successfully as/in : {fname}")
else:
    exit(f"Error occured!! Check URL and try again.\n\nError Code : {r.status_code}")
