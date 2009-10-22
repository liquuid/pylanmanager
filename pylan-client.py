#!/usr/bin/env python
import urllib, time, os, subprocess



configuracao = open('/etc/pylan-client.conf').read()
for i in configuracao.split():
	if i.split('=')[0]=="server":
		server_ip = i.split('=')[1]
	if i.split('=')[0]=="interface":
		interface = i.split('=')[1]

command = 'LANG=C ifconfig '+interface+' | grep "inet add" | cut -d ":" -f 2| sed "s/ //g" | sed "s/Bcast//g"'

proc = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
os.waitpid(proc.pid,0)
ip = proc.stdout.read().strip()


while 1:
	h = urllib.urlopen('http://'+server_ip+':8000/'+ip)
	tempo = h.read()
	tempo = tempo.strip()
	if int(tempo) > 0:
		print tempo
	else:
		print "tempo acabou"
		#os.system('killall -9 xterm')

	time.sleep(1)
