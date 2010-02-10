#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
# vim:ts=4:sw=4:et
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Copyright 2010 Fernando Henrique R. Silva (liquuid@gmail.com)
# http://www.linuxmafia.com.br

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
