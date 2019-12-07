from subprocess import *
from webbrowser import open as browser
import os

cmd = 'powercfg /batteryreport'.split()

r = Popen(cmd,stdout=PIPE,stderr=PIPE,close_fds=True)

browser(f"file:///{os.getcwd()}/battery-report.html")
