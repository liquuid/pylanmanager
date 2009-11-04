#!/usr/bin/env python

import gtk,gobject,subprocess,os
import urllib
command = 'ifconfig wlan0 | grep "inet add" | cut -d ":" -f 2| sed "s/ //g" | sed "s/Bcast//g"'
proc = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
os.waitpid(proc.pid,0)
ip = proc.stdout.read().strip()
server = open('/etc/pylan-client.conf').read()
server_ip = server.split('=')[1].strip()

h = urllib.urlopen('http://'+server_ip+'/'+ip)
hud = h.read()

gnome_on = False
time = 0

class Clock(gtk.Window):
	def __init__(self,parent=None):
		gtk.Window.__init__(self)
		try:
			self.set_screen(parent.get_screen())
		except AttributeError:
			self.connect('destroy',lambda *w:gtk.main_quit())
		self.set_title('Tempo Restante')
		self.timer = gobject.timeout_add(1000,tempo,self)
		self.set_border_width(5)
		self.set_default_size(250,30)
		self.entry = gtk.Statusbar()
		self.context_id= self.entry.get_context_id('bla')
		self.add(self.entry)

def tempo(self):
	global time
	global gnome_on
	global hud
	print "#"*50
	h = urllib.urlopen('http://'+server_ip+':8000/'+ip)
	hud = h.read()
	hud = int(hud.strip())
	time = int(hud)
	hor = str(hud/3600)
	min = str((hud%3600)/60)
	seg = str((hud%3600)%60)
	hud = str(n(hor)+':'+n(min)+':'+n(seg))
	
	if time != 0 and not gnome_on:
		print "abrindo gnome"
		os.system('/home/liquuid/Projetos/pylanmanager/pylan-gtk.py &')
		os.system('gnome-session &')
		gnome_on = True
	if time == 0 and gnome_on:
		print "fechando gnome"
		killprocess() 

		gnome_on = False

	self.entry.push(self.context_id,str(hud))
	return True

def killprocess():
	comm_tty = 'ps u | grep tty | grep -v grep | awk \'{print $2}\''
	p = subprocess.Popen(comm_tty,stdout=subprocess.PIPE,shell=True)
	list_tty = p.stdout.read().split('\n')

	comm_pylan = 'ps u | grep pylan | grep -v grep | awk \'{print $2}\''
	p = subprocess.Popen(comm_pylan,stdout=subprocess.PIPE,shell=True)
	list_pylan = p.stdout.read().split('\n')
	
	comm_all = 'ps u | grep -v grep | awk \'{print $2}\''
	p = subprocess.Popen(comm_all,stdout=subprocess.PIPE,shell=True)
	list_all = p.stdout.read().split('\n')
	
	for i in list_pylan + list_tty:
		try:
			list_all.remove(i)
		except:
			print "lixo" 
	
	for i in list_all:
		os.system('kill -9 '+str(i))
	

def n(var):
	if len(var) < 2:
		return '0'+var
	else:
		return var


def main():
	global gnome_on
	Clock()
	print hud , gnome_on
	if int(hud) != 0:
		os.system('/home/liquuid/Projetos/pylanmanager/pylan-gtk.py &')
		os.system('gnome-session&')
		gnome_on = True

	gtk.main()

if __name__ == '__main__':
	main()
