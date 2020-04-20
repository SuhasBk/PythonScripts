#!/usr/bin/python3

import pyautogui as win

class WhatsApp:
    def __init__(self):
        win.press("win")
        win.write("whatsapp", interval=0.25)
        win.press("enter")

if __name__ == '__main__':
    wapp = WhatsApp()
