#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import gtk,gobject,os
import urllib,pylanrc
import socket
server_ip = pylanrc.get_serverip()
interface = pylanrc.get_interface()
ip = pylanrc.get_ip()

print 'http://'+server_ip+'/'+ip

hud = 0
gnome_on = False
first_run=False
time=0
aviso5min=False

try:
	os.system('qiv --root /srv/pylan/bg.png')
except:
	print 'qiv not found'

class Clock(gtk.Window):
	"""  Classe gtk para controle de loop e futuras extencoes na tela """
	def __init__(self,parent=None):
		gtk.Window.__init__(self)
		try:
			self.set_screen(parent.get_screen())
		except AttributeError:
			self.connect('destroy',lambda *w:gtk.main_quit())
		self.set_title('Tempo Restante')
		self.timer = gobject.timeout_add(10000,tempo,self)
		self.internal = gobject.timeout_add(1000,internal_clock,self)

def get_time():
	""" funcao que contacta o servidor e retorna o tempo restante da sessao """
	try:	
		socket.setdefaulttimeout(1)
		h = urllib.urlopen('http://'+server_ip+'/'+ip)
		hud=h.read().strip()
		return int(hud)
	except IOError: 
		print 'Sem contato com o servidor'
		return 'Sem contato com o servidor'

def internal_clock(self):
	""" funcao que conta o tempo em paralelo com o servidor """
	global time
	if time >0:
		time = time - 1
	if time == 0 and first_run:
		killprocess()
	print time
	return True

def tempo(self):
	""" Loop executado a cada 10 segundos, responsavel por toda verificacao
	dos tempos de sessao e controle de fluxo do programa """
	global gnome_on
	global hud
	global first_run
	global time
	global aviso5min

	hud = get_time()
	if type(hud) == int: 
		if int(hud) != 0 and not gnome_on:
			print "abrindo gnome"
			time = hud
			os.system('/srv/pylan/pylan-clock.py &')
			os.system('gnome-session ?> /dev/null &')
			gnome_on = True
			first_run=True
		if int(hud) == 0 and first_run:
			killprocess() 
			gnome_on = False
		time = hud

		if int(hud) < 300 and int(hud) != 0 and not aviso5min :
			aviso5min=True
			os.system('zenity --info --text "Faltam 5 minutos para o término da sessão. \n \n Salve seus arquivos abertos" --title "Salve seus arquivos" &')		
		
		
		print 't='+str(hud)+'g='+str(gnome_on)+'f='+str(first_run)
	return True

def killprocess():
	""" Rotina para encerrar a sessao """
	print "fechando gnome"
	os.system('find /home/livre/ ! -name ".xinitrc" -exec rm -rf {} \;')
	os.system('cp -r /var/local/livre/ /home/')
	exit()	

def main():
	""" funcao principal """
	global gnome_on
	Clock()
	
	# 
	if int(hud) != 0:
		os.system('/srv/pylan/pylan-clock.py &')
		os.system('gnome-session 2> /dev/null &')
		gnome_on = True

	gtk.main()

if __name__ == '__main__':
	main()
