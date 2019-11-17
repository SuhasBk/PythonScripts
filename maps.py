#!/usr/bin/python3
import webbrowser
import sys

try:
    webbrowser.open('https://www.google.com/maps/place/' + sys.argv[1])
except:
    place=input("Enter the name of the place you want to visit:\n")
    webbrowser.open('https://www.google.com/maps/place/' + place)
