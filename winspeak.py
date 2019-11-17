#!/usr/bin/python3
import pyttsx3

engine = pyttsx3.init()

def winspeak(s):
    engine.say(s)
    engine.runAndWait()
    return

while True: winspeak(input("Enter the phrase to read\n"))
