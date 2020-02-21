#!/usr/bin/python3

from subprocess import *
import os
import getpass
import re,time

def call(cmd):
    p=Popen(cmd,close_fds=True,stderr=PIPE,stdout=PIPE,shell=True)
    s=p.stdout.read().decode()
    return s

def lock():
    call("adb shell input keyevent 26")

def unlock():
    pin=getpass.getpass("Enter the PIN code to unlock your device\n")
    if len(pin)<4:
        exit("Wrong bubba!\n")
    call("adb shell input keyevent 26")
    call("adb shell input swipe 600 1900 600 1900 2000")
    call("adb shell input swipe 500 1900 500 100")
    call("adb shell input text "+pin)
    call("adb shell input keyevent 66")

def network():
    networks=['Toggle WiFi','Toggle Mobile Data','Toggle Bluetooth (requires ROOT access)','Toggle USB tethering']
    for p,q in enumerate(networks):
        print(str(p)+' >>> '+q)
    ch = int(input("Enter the choice\n"))
    if ch==0:
        if 'enabled' in call("adb shell dumpsys wifi | head -n 1"):
            state = 'disable'
        else:
            state = 'enable'
        call("adb shell svc wifi {}".format(state))
    if ch==1:
        if '2' in call("adb shell dumpsys telephony.registry |  grep mDataConnectionState"):
            call("adb shell svc data disable")
        else:
            call("adb shell svc data enable")
    if ch==2:
        state = input("Do you want to 'enable' or 'disable' Bluetooth?\n> ").lower()
        if state not in ['enable','disable']:
            print("\nBad state... Aborting\n")
            return
        else:
            if state == 'enable':
                state = 6
            else:
                state = 8
        print(state)
        call("adb shell su -c service call bluetooth_manager {}".format(state))
    if ch==3:
        state = input("Do you want to turn ON('1') or OFF('0') USB tethering?\n> ")
        call("adb shell service call connectivity 33 i32 {} s16 text".format(state))

def rand():
    randoms=['SWIPE UP','SWIPE DOWN','SWIPE LEFT/RIGHT','BACK','HOME','RECENTS','TAP ON A POINT ON SCREEN']
    for j,k in enumerate(randoms):
        print(str(j)+' >>> '+k)
    ch=eval(input("Enter the choice\n"))
    if ch==0:
        call("adb shell input swipe 500 1300 500 800")
    elif ch==1:
        call("adb shell input swipe 500 800 500 1300")
    elif ch==2:
        print("HINT : \nTo swipe RIGHT : maintain POSITIVE distance between 'X' axes.\nTo swipe LEFT : maintain NEGATIVE distance between 'X' axes")
        x1=input("Enter the 'X1' co-ordinate\n")
        x2=input("Enter the 'X2' co-ordinate\n")
        call("adb shell input swipe {} 500 {} 500".format(x1,x2))
    elif ch==3:
        call("adb shell input keyevent 4")
    elif ch==4:
        call("adb shell input keyevent 3")
    elif ch==5:
        call("adb shell input keyevent KEYCODE_APP_SWITCH")
    elif ch==6:
        x=input("Enter the 'X' co-ordinate\n")
        y=input("Enter the 'Y' co-ordinate\n")
        call("adb shell input tap "+x+" "+y)

def tel():
    number = input("Enter the phone number\n> ")
    call("adb shell am start -a android.intent.action.CALL -d tel:"+number)

def sms():
    number = input("Enter the phone number\n> ")
    body = input("Enter the message you wish to send...\n")

    #call('adb shell service call isms 7 i32 0 s16 "com.android.mms.service" s16 "+91{0}" s16 "null" s16 "{1}" s16 "null" s16 "null"'.format(number,body))

    call('adb shell am start -a android.intent.action.SENDTO -d sms:91{} --es sms_body "{}";'.format(number,body))
    time.sleep(1)
    call("adb shell input mouse tap 980 1700")

def backdoor():
    while True:
        print('\nWelcome to bakcdoor entry...\n')
        cmd = input("Enter the ADB shell command... without 'adb shell' in the command\n")
        if cmd == 'exit':
            return
        call(f"adb shell {cmd}")

def cya():
    exit("BYE\n")

check=call("adb devices")
if(len(re.findall(r'(\w+)[\t]*device',check,re.IGNORECASE))<1):
    print("Make sure an Android device is connected and configured for USB/tcpip debugging")
else:
    l = input("Is the device locked?\n")
    if l in ['yes','y','yep']:
        unlock()
    elif l=='':
        print(l)
        exit("Please answer the goddamn question!".upper())

    func=['SEND SMS','PLACE A CALL','TOGGLE NETWORK STATUS','RANDOM ACTIONS','LOCK SCREEN','UNLOCK SCREEN','CUSTOM ADB COMMANDS','EXIT']

    routes = {0:sms,1:tel,2:network,3:rand,4:lock,5:unlock,6:backdoor,7:cya}

    try:
        while True:
            for i,j in enumerate(func):
                print(str(i)+' >>> '+j)
            f = int(input("\nEnter your choice\n"))
            if f in routes:
                routes[f]()
            else:
                print('Wrong choice...\n')
    except KeyboardInterrupt:
        exit("bye")
