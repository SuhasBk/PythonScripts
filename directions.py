#!/usr/bin/python3
import webbrowser
import sys

if len(sys.argv[1:]) != 2:
    src = input("Enter the source...\n> ")
    dest = input("Enter the destination...\n> ")
else:
    src = sys.argv[1]
    dest = sys.argv[2]

webbrowser.open("https://maps.google.com/maps?saddr={}&daddr={}".format(src,dest))
