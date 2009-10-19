#!/usr/bin/env python

import gtk,gobject
import urllib

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
		self.show_all()

def tempo(self):
	try:
		h = urllib.urlopen('http://localhost:8000/192.168.0.1')
		hud = h.read()
		hud = int(hud.strip())
		hor = str(hud/3600)
		min = str((hud%3600)/60)
		seg = str((hud%3600)%60)
		hud = str(n(hor)+':'+n(min)+':'+n(seg))
	except:
		hud = 'sem contato com o servidor'

	self.entry.push(self.context_id,str(hud))
	return True

def n(var):
	if len(var) < 2:
		return '0'+var
	else:
		return var


def main():
	Clock()
	gtk.main()

if __name__ == '__main__':
	main()
