from subprocess import Popen,PIPE
import webbrowser
import os

cmd = 'powercfg /batteryreport'.split()

r = Popen(cmd,stdout=PIPE,stderr=PIPE,close_fds=True)

webbrowser.open(f"file:///{os.getcwd()}/battery-report.html")
