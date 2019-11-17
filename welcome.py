#!/usr/bin/python3
import pyttsx3
import time
import os
import webbrowser

def Welcome():
    lta=time.ctime().split(' ')[3]
    std='12:00:00'
    std1='16:00:00'
    std2='00:00:00'
    std3='05:00:00'
    std4='20:59:00'

    if lta>std3 and lta<std:
        print("Good Morning!!\n")
    elif lta>std and lta<std1:
        print("Good Afternoon!\n")
    elif lta>std1 and lta<std4 :
        print("Good Evening!\n")
    elif lta>std1 and lta<std2:
        print("Good night!\n")
    elif lta>std2 and lta<std3:
        print("New Day!\n")
    elif lta>std4 and lta<std2:
        print("Good night!\n")
    else:
        print("Good Night\n")

    print("Hey buddy!")
    fuck=pyttsx3.init()
    fuck.say("Hey buddy!")
    fuck.runAndWait()
    print('The geek lord welcomes you. The machine is up and running to serve you, all programs hail the master!')
    fuck.say("the geek lord welcomes you. The machine is up and running to serve you, all programs hail the master! longlive python, longlive the user")
    fuck.runAndWait()

Welcome()

def Closing():
    fuck=pyttsx3.init()
    print("THIS IS NOT A DRILL. I can also shutdown if you want me to...")
    fuck.say("THIS IS NOT A DRILL. I can also shutdown if you want me to...")
    fuck.runAndWait()
    print("PRESS 1 TO SHUTDOWN")
    time.sleep(0.5)
    print("PRESS 2 TO HIBERNATE")
    time.sleep(0.5)
    print("PRESS 3 TO RESTART")
    time.sleep(0.5)
    choice=input("Whats it gonna be boy?\n")

    if choice == '1':
        os.system("shutdown -t 0 /s /f")
    elif choice == '2':
        os.system("shutdown /h")
    elif choice == '3':
        os.system("shutdown -t 0 /r /f")
    else:
        print("Wrong Input")
        exit()

def Operations():
    fuck=pyttsx3.init()
    print('Also, I can do some pretty basic shit like --')
    fuck.say('Also, I can do some pretty basic shit like...')
    fuck.runAndWait()
    fuck.say(" show your music directory or start your games and shit like that. So who's cool now?! Me or Siri?")
    fuck.runAndWait()
    print(" TYPE 'MUSIC' TO OPEN YOUR SEXY MUSIC LIBRARY")
    print(" TYPE 'CS' TO PLAY COUNTER STRIKE 1.6")
    print(" TYPE 'BROWSER' TO BROWSE THE WEB")
    print(" TYPE 'GUI' TO DISPLAY TkINTER GUI")
    print(" JUST PRESS ANYTHING TO CLOSE THIS SCREEN")
    choice=input()
    shit=choice.upper()
    print(("You have chosen - "+shit.upper()))

    if(shit == 'MUSIC'):
        print("Let's Party")
        fuck.say("Let's party")
        fuck.runAndWait()
        webbrowser.open("D:\MUSIC")
        exit()

    elif(shit == 'CS'):
        print("Let's Play. I thought you would like some music too. Haha, thank me later.")
        fuck.say("lets play. I thought you would like some music too. Haha, thank me later.")
        fuck.runAndWait()
        webbrowser.open("D:\MUSIC")
        webbrowser.open("C:/Users/acer/Desktop/Counter-Strike 1.6/cstrike.exe")
        exit()

    elif(shit == 'BROWSER'):
        print("Let's browse Internet. How about that?")
        fuck.say("Let's browse the shit out of internet. How about that?")
        fuck.runAndWait()
        webbrowser.open("http://google.com")
        exit()

    elif(shit == "GUI"):
        print("Buckle up! Exciting stuff coming your way!")
        fuck.say("Buckle up! Exciting stuff coming your way!")
        fuck.runAndWait()
        webbrowser.open("D:/Documents/My summer stuff/GUI/GUI.py")
        exit()

    else:
        print("Wrong choice. Self-destructing sequence initiated by user\nBOOM!")
        fuck.say("wrong choice. self destructing sequence initiated by user")
        fuck.runAndWait()
        Closing()

Operations()
Closing()
