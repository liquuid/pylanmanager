#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import gtk,gobject
import pylanrc
import urllib

server_ip = pylanrc.get_serverip()
interface = pylanrc.get_interface()
ip = pylanrc.get_ip()

print server_ip , interface, ip

class Clock(gtk.Window):
	""" Classe que cria objeto contador de tempo """
	def __init__(self,parent=None):
		""" Construtor do nosso contador de tempo """
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
	""" Função que adquire o tempo restante no servidor """
	try:
		h = urllib.urlopen('http://'+server_ip+'/'+ip)
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
	""" Recebe um número com um digito e retorna o mesmo numero com um zero na frente """
	if len(var) < 2:
		return '0'+var
	else:
		return var


def main():
	Clock()
	gtk.main()

if __name__ == '__main__':
	main()
