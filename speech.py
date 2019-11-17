#!/usr/bin/python3
import time
import pyttsx3
import speech_recognition as sr
from subprocess import run,PIPE

r = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate','170')

hotword = 'jarvis'

def say(s):
    print(s)
    engine.say(s)
    engine.runAndWait()
    return

say("\nInvoke me with {}\n".format(hotword))

def listen():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source,phrase_time_limit=2)
        return audio

try:
    while True:
        print("\nInvoke me with {}\n".format(hotword))
        hot_word = r.recognize_google(listen())
        if hotword in hot_word.lower():
            say("\nHey fella! What's your name buddy?")
            name = r.recognize_google(listen())
            say("Hello! "+name)
        time.sleep(0.5)

except sr.UnknownValueError:
    pass
except KeyboardInterrupt:
    say("\nBye buddy... nice chatting with you\n")
