#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

r = requests.get("http://dollarrupee.in/")
s = BeautifulSoup(r.text,'html.parser')
p = s.select('p > strong')
rate = float(p[0].text)

print("Today's exchange rate : {}\n".format(rate))

print("1 - USD to INR\n2 - INR to USD\n")
ch = input("Please enter the choice:\n> ")

amt = float(input("Enter the amount : ").replace(',',''))

if ch == '1':
    print("{} in USD equals {} in INR".format(amt,round(amt*rate)))

elif ch == '2':
    print("{} in INR equals {} in USD".format(amt,round(amt/rate)))
