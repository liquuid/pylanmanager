#!/usr/bin/env python

import gtk,gobject,os
import urllib,pylanrc
server_ip = pylanrc.get_serverip()
interface = pylanrc.get_interface()
ip = pylanrc.get_ip()

print 'http://'+server_ip+'/'+ip

#if get_time():
#	hud = get_time()
hud = 0
gnome_on = False
first_run=False
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
def get_time():
	try:
		h = urllib.urlopen('http://'+server_ip+'/'+ip)
		hud=h.read()
		return hud
	except IOError: 
		print 'Sem contato com o servidor'

def tempo(self):
	global time
	global gnome_on
	global hud
	global first_run
#	try:
#		h = urllib.urlopen('http://'+server_ip+'/'+ip)
#		hud=h.read()
#	except IOError: 
#		print 'Sem contato com o servidor'
	if get_time():
		hud = get_time()
		hud = int(hud.strip())
		time = int(hud)
		hor = str(hud/3600)
		min = str((hud%3600)/60)
		seg = str((hud%3600)%60)
		hud = str(n(hor)+':'+n(min)+':'+n(seg))
	
	if time != 0 and not gnome_on:
		print "abrindo gnome"
		os.system('/srv/pylan/pylan-clock.py &')
		os.system('gnome-session ?> /dev/null &')
		gnome_on = True
		first_run=True
	if time == 0 and first_run:
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
		os.system('/srv/pylan/pylan-clock.py &')
		os.system('gnome-session 2> /dev/null &')
		gnome_on = True

	gtk.main()

if __name__ == '__main__':
	main()
