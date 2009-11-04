#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import gobject
import gtk
from datetime import datetime
from time import time
import sys
import os

class Users(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_border_width(5)
        self.set_default_size(640, 400)
#	self.timer = gobject.timeout_add(1000,tempo,self)
	self.vars=[]

	vbox = gtk.VBox(True, 5)
	vboxp= gtk.VBox(False, 5)
	vbox2= gtk.VBox(False, 5)
	vbox3= gtk.VBox(False, 5)
	vbox4= gtk.VBox(False, 5)
	vbox5= gtk.VBox(False, 5)
	vbox6= gtk.VBox(False, 5)

	hbox = gtk.HBox(False, 1) 
	hbox2 = gtk.HBox(False,1)	
	hbox3 = gtk.HBox(False,1)	
	hbox4 = gtk.HBox(False,1)
	hbox5 = gtk.HBox(False,1)
	hbox6 = gtk.HBox(False,1)
	hbox7 = gtk.HBox(False,1)

	frame = gtk.Frame('Identificação')
	frame2 = gtk.Frame('Contato')
	frame3 = gtk.Frame('Controle')
	frame4 = gtk.Frame('Busca')

	label_name = gtk.Label("Nome")
	label_idade = gtk.Label("Idade")
	label_birth = gtk.Label("Data de Nascimento")
	label_sex = gtk.Label("Sexo")
	label_id = gtk.Label("RG/CPF")
	label_esco = gtk.Label("Escolaridade")
	label_tel = gtk.Label("Telefone")
	label_email = gtk.Label("Email")	
	label_addr = gtk.Label("Endereço")
	label_cep = gtk.Label("CEP")
	label_search = gtk.Label("Busca por RG/CPF") 
	label_name.set_justify(gtk.JUSTIFY_RIGHT)
	label_name.set_justify(gtk.JUSTIFY_RIGHT)
	
	entry_name  = gtk.Entry()
	entry_idade  = gtk.Entry(max=3)
	entry_id = gtk.Entry(max=10)
	entry_birth  = gtk.Entry(max=10)
	entry_sex=gtk.combo_box_new_text()
	entry_sex.append_text("Feminino")
	entry_sex.append_text("Masculino")
	entry_search = gtk.Entry(max=10)

	entry_esco  = gtk.Entry(max=20)
	entry_tel  = gtk.Entry(max=15)
	entry_email  = gtk.Entry(max=50)
	entry_addr  = gtk.Entry(max=300)
	entry_cep  = gtk.Entry(max=10)
	

	vbox.pack_start(label_name)
	vbox2.pack_start(entry_name)
	vbox.pack_start(label_id)
	vbox2.pack_start(entry_id)
	vbox.pack_start(label_sex)
	vbox2.pack_start(entry_sex)
	vbox.pack_start(label_idade)
	vbox2.pack_start(entry_idade)
	vbox.pack_start(label_birth)
	vbox2.pack_start(entry_birth)
	vbox.pack_start(label_esco)
	vbox2.pack_start(entry_esco)
	
	vbox3.pack_start(label_addr)
	vbox4.pack_start(entry_addr)
	vbox3.pack_start(label_cep)
	vbox4.pack_start(entry_cep)
	vbox3.pack_start(label_tel)
	vbox4.pack_start(entry_tel)
	vbox3.pack_start(label_email)
	vbox4.pack_start(entry_email)

#	self.statusbar = gtk.Statusbar()
#	hbox.pack_start(self.statusbar,True,True,0)
#	self.context_id = self.statusbar.get_context_id("context_description")
#	self.statusbar.show()

	button_add = gtk.Button(stock=gtk.STOCK_ADD)
	button_clear = gtk.Button(stock=gtk.STOCK_CLEAR)
	button_search = gtk.Button(stock=gtk.STOCK_FIND)
	vboxp.pack_start(hbox7)
	vboxp.pack_start(hbox)
	vboxp.pack_start(hbox5)
	vboxp.pack_start(hbox6)

	hbox.pack_start(hbox2)
	hbox2.pack_start(frame)
	hbox2.pack_start(frame3)
	hbox5.pack_start(frame2)

#	hbox6.pack_start(frame4)

	hbox6.pack_start(button_add)
	hbox6.pack_start(button_clear)

	hbox7.pack_start(label_search)
	hbox7.pack_start(entry_search)
	hbox7.pack_start(button_search)

	hbox3.pack_start(vbox,False,False,5)
	hbox3.pack_start(vbox2)

	hbox4.pack_start(vbox3,False,False,50)
	hbox4.pack_start(vbox4)

	frame.add(hbox3)
	frame2.add(hbox4)
	self.add(vboxp)

	self.show_all()
    
    def timeout(self,i):
    	if (int(maquinas[i][1])+int(maquinas[i][2]*60)-int(time()))/60.0 < 0:
		return True
	else:
		return False


    def __showvars(self,button,model):
	while 1:
		while gtk.events_pending():gtk.main_iteration()
		print datetime.now()
    def cancelseasson(self,button,i):
	maquinas[i][1] = 0


    def add15(self,button,i):
	if self.timeout(i):
		maquinas[i][1] = int(time())
		maquinas[i][2] = 15
	else:
		maquinas[i][2] = maquinas[i][2] + 15
    def add30(self,button,i):
	if self.timeout(i):
		maquinas[i][1] = int(time())
		maquinas[i][2] = 30
	else:
		maquinas[i][2] = maquinas[i][2] + 30

    def add60(self,button,i):
	if self.timeout(i):
		maquinas[i][1] = int(time())
		maquinas[i][2] = 60
	else:
		maquinas[i][2] = maquinas[i][2] + 60


def tempo(self):
	for i in range(len(self.vars)):
		if (int(maquinas[i][1])+int(maquinas[i][2]*60)-int(time()))/60.0 < 1 and (int(maquinas[i][1])+int(maquinas[i][2]*60)-int(time()))/60.0 > 0:
			self.vars[i].set_text(str((int(maquinas[i][1])+int(maquinas[i][2]*60)-int(time())))+" segundos")
		elif	self.timeout(i):
			self.vars[i].set_text(str("Encerrado"))
			fd = open(os.path.expanduser('~/')+'.pyland/'+maquinas[i][3],'w')
			fd.write(str(0))
			fd.close()

		elif 	not self.timeout(i):
			self.vars[i].set_text(str((int(maquinas[i][1])+int(maquinas[i][2]*60)-int(time())+60)/60)+" minutos")
		
		if not self.timeout(i):
			fd = open(os.path.expanduser('~/')+'.pyland/'+maquinas[i][3],'w')
			fd.write(str(int(maquinas[i][1])+int(maquinas[i][2]*60)-int(time())))
			fd.close()


	self.statusbar.push(self.context_id,str(datetime.now()))
	return True


def main():
    Users()
    gtk.main()

if __name__ == '__main__':
    main()

