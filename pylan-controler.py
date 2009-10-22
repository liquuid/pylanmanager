#!/usr/bin/env python

import gtk,gobject,subprocess,os
import urllib
command = 'ifconfig wlan0 | grep "inet add" | cut -d ":" -f 2| sed "s/ //g" | sed "s/Bcast//g"'
proc = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
os.waitpid(proc.pid,0)
ip = proc.stdout.read().strip()
server = open('/etc/pylan-client.conf').read()
server_ip = server.split('=')[1].strip()

h = urllib.urlopen('http://'+server_ip+':8000/'+ip)
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
		#self.show_all()

def tempo(self):
	global time
	global gnome_on
	global hud
	print int(time),int(hud),gnome_on
	try:	
		print "tentando"
		h = urllib.urlopen('http://'+server_ip+':8000/'+ip)
		hud = h.read()
		hud = int(hud.strip())
		time = int(hud.strip())
		hor = str(hud/3600)
		min = str((hud%3600)/60)
		seg = str((hud%3600)%60)
		hud = str(n(hor)+':'+n(min)+':'+n(seg))
	except:
		hud = 'Sem contato com o servidor'
	
	if time != 0 and not gnome_on:
		print "abrindo gnome"
		os.system('/home/liquuid/Projetos/pylanmanager/pylan-gtk.py &')
		os.system('gnome-session &')
		gnome_on = True
	print time
	if time == 0 and gnome_on:
		print "fechando gnome"
		os.system('gnome-session-save --force-logout')
		gnome_on = False
	#if time == 0 and not gnome_on:
#		os.system('/home/liquuid/Projetos/pylanmanager/pylan-gtk.py &')
#		os.system('gnome-session &')
#		gnome_on = True

	self.entry.push(self.context_id,str(hud))
	return True


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
		print "first"
		os.system('/home/liquuid/Projetos/pylanmanager/pylan-gtk.py &')
		os.system('gnome-session &')
		gnome_on = True

	gtk.main()

if __name__ == '__main__':
	main()
