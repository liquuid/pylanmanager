#!/usr/bin/env python

import gtk,gobject,subprocess,os
import urllib
configuracao = open('/etc/pylan-client.conf').read()
for i in configuracao.split():
        if i.split('=')[0]=="server":
                server_ip = i.split('=')[1]
        if i.split('=')[0]=="interface":
                interface = i.split('=')

command = 'LANG=C ifconfig wlan0 | grep "inet add" | cut -d ":" -f 2| sed "s/ //g" | sed "s/Bcast//g"'
proc = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
os.waitpid(proc.pid,0)
ip = proc.stdout.read().strip()
print 'http://'+server_ip+'/'+ip
h = urllib.urlopen('http://'+server_ip+'/'+ip)
hud = h.read()

gnome_on = False
time = 0

try:
	os.system('qiv --root /srv/pylan/bg.png')
except:
	print 'qiv not found'

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
#	print "#"*50
	h = urllib.urlopen('http://'+server_ip+'/'+ip)
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
		os.system('gnome-session ?> /dev/null &')
		gnome_on = True
	if time == 0 and gnome_on:
		print "fechando gnome"
		killprocess() 

		gnome_on = False

	self.entry.push(self.context_id,str(hud))
	return True

def killprocess():
	exit()	

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
		os.system('gnome-session 2> /dev/null &')
		gnome_on = True

	gtk.main()

if __name__ == '__main__':
	main()
