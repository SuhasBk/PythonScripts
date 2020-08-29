#!/usr/local/bin/python3
from subprocess import Popen,PIPE
import sys

def start(app_name: str, *args):
    root_app = [app_name]

    if sys.platform.startswith('linux') or sys.platform.startswith('win32'):
        root_app.extend(args)
        Popen(root_app)
    elif sys.platform.startswith('darwin'):
        try:
            args = [*args]
            command = ["open", "-a"]
            command.extend([*root_app, '--args', *args])
            p = Popen(command, stderr=PIPE)
            error = p.stderr.read()
            if error != b'':
                raise Exception(error)
        except Exception as e:
            print(e)
            root_app.extend(args)
            Popen(root_app)
    
