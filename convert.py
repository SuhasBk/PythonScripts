#!/usr/bin/python3
import requests
from bs4 import *

r=requests.get("http://dollarrupee.in/")
s=BeautifulSoup(r.text,'html.parser')
p=s.select('p>strong')
rate=float(p[0].text)

print("Today's exchange rate : {}\n".format(rate))

print("1 - USD to INR\n2 - INR to USD\n")
ch = input("Please enter the choice:\n> ")

if ch == '1':
    amt = float(input("Enter the amount in USD : "))
    print("{} in USD equals {} in INR".format(amt,round(amt*rate)))

elif ch == '2':
    amt = float(input("Enter the amount is INR : "))
    print("{} in INR equals {} in USD".format(amt,round(amt/rate)))
