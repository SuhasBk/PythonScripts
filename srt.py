#!/usr/bin/python3
from selenium import webdriver

mt=input("Enter the title of the movie/tv series:\n")
try:
    s,e=input("Enter season and episode number seperated by a space (just press 'enter' if its a movie)\n").split(" ")
except:
    s=e=''
    pass

b=webdriver.Firefox()
print("Searching....\n")
if s=='' or e=='':
    b.get("https://subtitleslive.com/"+'-'.join(mt.split(" ")))
else:
    b.get("https://subtitleslive.com/"+'-'.join(mt.split(" "))+"/season-"+s+"/episode-"+e)

b.execute_script("window.scrollTo(0,3000)")
b.execute_script("window.alert('Click on any one of these subtitles to download ;)')")
