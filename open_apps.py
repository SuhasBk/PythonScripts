#!/usr/bin/python3
from subprocess import Popen,PIPE
import sys

def start(app_name,*args):
    root_app = [app_name]

    if sys.platform.startswith('linux') or sys.platform.startswith('win32'):
        root_app.extend(args)
        Popen(root_app)
    else:
        args = [*args]
        command = ["open","-a"]
        command.extend([*root_app,*args])
        Popen(command)
    
