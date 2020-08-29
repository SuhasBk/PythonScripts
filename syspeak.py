#!/usr/local/bin/python3
import pyttsx3

engine = pyttsx3.init()

def syspeak(s):
    engine.say(s)
    engine.runAndWait()
    return

while True: syspeak(input("Enter the phrase to read\n"))
