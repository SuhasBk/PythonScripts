#!/usr/local/bin/python3
import smtplib
from getpass import getpass

TO = input("Enter the recepient's email id...\n")
SUBJECT = 'GREETINGS!'
TEXT = input("Enter the text message here...\n")
gmail_sender = input("Enter your Email-ID\n")
gmail_passwd = getpass("Enter the password\n")

server = smtplib.SMTP('smtp.gmail.com',587)         #server for gmail
server.ehlo()                                       #connection to server
server.starttls()                                   #security layer
#server.ehlo
server.login(gmail_sender,gmail_passwd)             #login to server

BODY = '\r\n'.join([
    'To: %s' % TO,
    'From :%s' % gmail_sender,
    'Subject: %s' % SUBJECT,
    '',
    TEXT
    ])

try:
    server.sendmail(gmail_sender, [TO], BODY)       #send mail
    print('Email sent')
except:
    print('Something went wrong. Sorry for the inconvenience. Please try again later\n')

server.quit()                                       #stop the server
