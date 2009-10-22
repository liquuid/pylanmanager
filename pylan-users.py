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

	table = gtk.Table(2,8,False)
	self.add(table)
	vbox = gtk.VBox(False, 5)
	vbox2= gtk.VBox(False, 5)
	vbox3= gtk.VBox(False, 5)
	vbox4= gtk.VBox(False, 5)
	vbox5= gtk.VBox(False, 5)
	vbox6= gtk.VBox(False, 5)

	hbox = gtk.HBox(False, 1) 

	table.attach(vbox,0,1,0,1)
	table.attach(vbox2,1,2,0,1)
	table.attach(vbox3,2,3,0,1)
	table.attach(vbox4,4,5,0,1)
	table.attach(vbox5,5,6,0,1)
	table.attach(vbox6,6,7,0,1)
	table.set_col_spacing(1,20)

	label_name = gtk.Label("Nome")
	label_idade = gtk.Label("Idade")
	label_birth = gtk.Label("Data de Nascimento")
	label_sex = gtk.Label("Sexo")
	label_esco = gtk.Label("Escolaridade")
	label_tel = gtk.Label("Telefone")
	label_email = gtk.Label("Email")	
	label_addr = gtk.Label("Endereço")
	label_cep = gtk.Label("CEP")

	entry_name  = gtk.Entry()
	entry_idade  = gtk.Entry()
	entry_birth  = gtk.Entry()
	entry_sex  = gtk.Entry()
	entry_esco  = gtk.Entry()
	entry_tel  = gtk.Entry()
	entry_email  = gtk.Entry()
	entry_addr  = gtk.Entry()
	entry_cep  = gtk.Entry()
	

	vbox.pack_start(label_name)
	vbox2.pack_start(entry_name)
	vbox.pack_start(label_sex)
	vbox2.pack_start(entry_sex)
	vbox.pack_start(label_idade)
	vbox2.pack_start(entry_idade)
	vbox.pack_start(label_birth)
	vbox2.pack_start(entry_birth)
	vbox.pack_start(label_esco)
	vbox2.pack_start(entry_esco)
	vbox.pack_start(label_addr)
	vbox2.pack_start(entry_addr)
	vbox.pack_start(label_cep)
	vbox2.pack_start(entry_cep)
	vbox.pack_start(label_tel)
	vbox2.pack_start(entry_tel)
	vbox.pack_start(label_email)
	vbox2.pack_start(entry_email)

#	for i in range(len(maquinas)):
#	        button = gtk.Button(stock="Adicionar 30 minutos")
#		button.connect("clicked", self.add30,i)
#        	vbox4.pack_start(button)
	
#	self.statusbar = gtk.Statusbar()
#	hbox.pack_start(self.statusbar,True,True,0)
#	self.context_id = self.statusbar.get_context_id("context_description")
#	self.statusbar.show()
       	table.attach(hbox,0,7,7,8)

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

