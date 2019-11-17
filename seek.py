#!/usr/bin/python3
import webbrowser,sys

if len(sys.argv[1:]) < 1:
    search_term = ' '.join(input("Enter the search term\n").split())
else:
    search_term = ' '.join(sys.argv[1:])

webbrowser.open("http://google.com/search?q="+search_term)
