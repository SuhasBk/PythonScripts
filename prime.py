#!/usr/bin/python3
import webbrowser
import sys

try:
    search_parameter = ' '.join(sys.argv[1:])
except IndexError:
    search_parameter = ''

webbrowser.open(f"https://www.primevideo.com/search/?phrase={search_parameter}")

