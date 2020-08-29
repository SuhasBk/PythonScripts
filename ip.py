#!/usr/local/bin/python3
import sys,re
from subprocess import Popen,PIPE

if sys.platform.startswith('win'):
    op = Popen('ipconfig',stdout=PIPE).communicate()[0]
else:
    op = Popen('ifconfig',stdout=PIPE).communicate()[0]

curr_ip = re.findall(r'192.168.[0-1].[\d+]*',str(op))

print("This computer's possible local Ipv4 address are :\n\n{}\n".format(set(curr_ip)))
