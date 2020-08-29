#!/usr/local/bin/python3
import sys
from speech_recognition import *

mic = Microphone()
rz = Recognizer()

with mic as source:
    audio = rz.listen(source)

open('cool.wav','ba+').write(audio.get_wav_data())
