#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import gobject
import gtk
from datetime import datetime
from time import time
import sys
import os
import sqlite3

try:
	arquivo = open(os.path.expanduser('~/')+'.pylanrc','r')
	arquivo.close()
except IOError:
	print "criando arquivo de configuracao"
	arquivo = open(os.path.expanduser('~/')+'.pylanrc','w')
	arquivo.write('pc1,192.168.0.1\npc2,192.168.0.2\n\n')
	arquivo.close()


try:
	os.mkdir(os.path.expanduser('~/')+'.pyland')
except:
	print 'diretorio .pyland já existe'


try: 
	db_file = open(os.path.expanduser('~/')+'.pylandb.sqlite3','r')
	db_file.close()
except:
	print 'criando database'
	connection = sqlite3.connect(os.path.expanduser('~/')+'.pylandb.sqlite3')
	cur = connection.cursor()
	cur.execute('CREATE TABLE users(id NUMBER,name VARCHAR,gender BOOLEAN,birthday VARCHAR,grad NUMBER,address VARCHAR,zip VARCHAR,phone VARCHAR,email VARCHAR)')
	cur.execute('insert into users (id,name,gender,birthday,grad,address,zip,phone,email) VALUES(341480138,\'fernanda\',\'False\',\'11/05/1980\',1,\'asf\',\'123-123\',\'123-123\',\'qwqe\');')
	cur.execute('insert into users (id,name,gender,birthday,grad,address,zip,phone,email) VALUES(341480137,\'fernando\',\'True\',\'11/05/1981\',1,\'asf\',\'123-123\',\'123-123\',\'qwqe\');')
	connection.commit()
	
	


maquinas=[]

config = open(os.path.expanduser('~/')+'.pylanrc','r')
cfd = config.read()
for i in range(len(cfd.split('\n'))-2):
	maquinas.append([cfd.split('\n')[i].split(',')[0],0,0,cfd.split('\n')[i].split(',')[1],True])
	
config.close()

#   columns
(
  COLUMN_NAME,
  COLUMN_START,
  COLUMN_TIME,
  COLUMN_IP,
  COLUMN_EDITABLE
) = range(5)


class EditBox(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
	self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.win.destroy()
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_border_width(5)
        self.set_default_size(640, 400)
	self.timer = gobject.timeout_add(1000,tempo,self)
        self.vars = []
	vbox = gtk.VBox(False, 5)
        self.add(vbox)

        label = gtk.Label("Lista de máquinas (editavel)")
        vbox.pack_start(label, False, False)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw)

        # create model
        model = self.__create_model()

        # create tree view
        treeview = gtk.TreeView(model)
        treeview.set_rules_hint(True)
        treeview.get_selection().set_mode(gtk.SELECTION_SINGLE)

        self.__add_columns(treeview)
        sw.add(treeview)

        # some buttons
        hbox = gtk.HBox(True, 4)
        vbox.pack_start(hbox, False, False)

        button = gtk.Button(stock=gtk.STOCK_ADD)
        button.connect("clicked", self.on_add_item_clicked, model)
        hbox.pack_start(button)

        button = gtk.Button(stock=gtk.STOCK_REMOVE)
        button.connect("clicked", self.on_remove_item_clicked, treeview)
        hbox.pack_start(button)
	button = gtk.Button(label="atcha")
	button.connect("clicked",self.__showvars)
	hbox.pack_start(button)

	self.statusbar = gtk.Statusbar()
	vbox.pack_start(self.statusbar,False,True,0)
	self.statusbar.show()
	self.context_id = self.statusbar.get_context_id("context_description")

        self.show_all()

    def __showvars(self,widget):
		self.destroy()
		return 0

    def __create_model(self):

        # create list store
        model = gtk.ListStore(
            gobject.TYPE_STRING,
            gobject.TYPE_STRING,
	    gobject.TYPE_INT,
	    gobject.TYPE_STRING,
            gobject.TYPE_BOOLEAN
       )

        # add items
        for item in maquinas:
            iter = model.append()

            model.set (iter,
                  COLUMN_NAME, item[COLUMN_NAME],
                  COLUMN_START, item[COLUMN_START],
		  COLUMN_TIME,item[COLUMN_TIME],
		  COLUMN_IP,item[COLUMN_IP],
                  COLUMN_EDITABLE, item[COLUMN_EDITABLE]
           )
        return model


    def __add_columns(self, treeview):

        model = treeview.get_model()

        # nome column
        renderer = gtk.CellRendererText()
        renderer.connect("edited", self.on_cell_edited, model)
        renderer.set_data("column", COLUMN_NAME)

        column = gtk.TreeViewColumn("Nome", renderer, text=COLUMN_NAME,
                               editable=COLUMN_EDITABLE)
        treeview.append_column(column)

        # start column
        renderer = gtk.CellRendererText()
        renderer.connect("edited", self.on_cell_edited, model)
        renderer.set_data("column", COLUMN_START)

        column = gtk.TreeViewColumn("Início", renderer, text=COLUMN_START,
                               editable=COLUMN_EDITABLE)
        treeview.append_column(column)

        # time column
        renderer = gtk.CellRendererText()
        renderer.connect("edited", self.on_cell_edited, model)
        renderer.set_data("column", COLUMN_TIME)

        column = gtk.TreeViewColumn("Tempo", renderer, text=COLUMN_TIME,
                               editable=COLUMN_EDITABLE)
        treeview.append_column(column)


        # ip column
        renderer = gtk.CellRendererText()
        renderer.connect("edited", self.on_cell_edited, model)
        renderer.set_data("column", COLUMN_IP)

        column = gtk.TreeViewColumn("IP", renderer, text=COLUMN_IP,
                               editable=COLUMN_EDITABLE)
        treeview.append_column(column)


    def on_add_item_clicked(self, button, model):
	new_item = ["pc", int(time()),0,0,"192.168.0.0", True]
        maquinas.append(new_item)

        iter = model.append()
        model.set (iter,
            COLUMN_NAME, new_item[COLUMN_NAME],
            COLUMN_START, new_item[COLUMN_START],
	    COLUMN_TIME, new_item[COLUMN_TIME],
	    COLUMN_IP, new_item[COLUMN_IP],
            COLUMN_EDITABLE, new_item[COLUMN_EDITABLE]
       )


    def on_remove_item_clicked(self, button, treeview):

        selection = treeview.get_selection()
        model, iter = selection.get_selected()

        if iter:
            path = model.get_path(iter)[0]
            model.remove(iter)

            del maquinas[ path ]


    def on_cell_edited(self, cell, path_string, new_text, model):

        iter = model.get_iter_from_string(path_string)
        path = model.get_path(iter)[0]
        column = cell.get_data("column")

        if column == COLUMN_NAME:
            maquinas[path][COLUMN_NAME] = new_text

            model.set(iter, column, maquinas[path][COLUMN_NAME])

        elif column == COLUMN_START:
            old_text = model.get_value(iter, column)
            maquinas[path][COLUMN_START] = int(new_text)

            model.set(iter, column, maquinas[path][COLUMN_START])
    	elif column == COLUMN_TIME:
		old_text = model.get_value(iter,column)
		maquinas[path][COLUMN_TIME] = int(new_text)

		model.set(iter,column, maquinas[path][COLUMN_TIME])
    	elif column == COLUMN_IP:
		old_text = model.get_value(iter,column)
		maquinas[path][COLUMN_IP] = new_text

		model.set(iter,column, maquinas[path][COLUMN_IP])


class Painel(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_border_width(5)
        self.set_default_size(640, 400)
	self.timer = gobject.timeout_add(1000,tempo,self)
	self.vars=[]
	notebook = gtk.Notebook()
	notebook.set_tab_pos(gtk.POS_TOP)
	
	mtable = gtk.Table(3,6,False)
	self.add(mtable)

########################################################################


        fvbox = gtk.VBox(True, 5)
        fvboxp= gtk.VBox(False, 5)
        fvbox2= gtk.VBox(False, 5)
        fvbox3= gtk.VBox(False, 5)
        fvbox4= gtk.VBox(False, 5)
        fvbox5= gtk.VBox(False, 5)
        fvbox6= gtk.VBox(False, 5)

        fhbox = gtk.HBox(False, 1)
        fhbox2 = gtk.HBox(False,1)
        fhbox3 = gtk.HBox(False,1)
        fhbox4 = gtk.HBox(False,1)
        fhbox5 = gtk.HBox(False,1)
        fhbox6 = gtk.HBox(False,1)
        fhbox7 = gtk.HBox(False,1)

        fframe = gtk.Frame('Identificação')
        fframe2 = gtk.Frame('Contato')
        fframe3 = gtk.Frame('Controle')
        fframe4 = gtk.Frame('Busca')

        flabel_name = gtk.Label("Nome")
        flabel_idade = gtk.Label("Idade")
        flabel_birth = gtk.Label("Data de Nascimento")
        flabel_sex = gtk.Label("Sexo")
        flabel_id = gtk.Label("RG/CPF")
        flabel_esco = gtk.Label("Escolaridade")
        flabel_tel = gtk.Label("Telefone")
        flabel_email = gtk.Label("Email")
        flabel_addr = gtk.Label("Endereço")
        flabel_cep = gtk.Label("CEP")
        flabel_search = gtk.Label("Busca por RG/CPF")
        flabel_name.set_justify(gtk.JUSTIFY_RIGHT)
        flabel_name.set_justify(gtk.JUSTIFY_RIGHT)

        fentry_name  = gtk.Entry()
        fentry_idade  = gtk.Entry(max=3)
        fentry_id = gtk.Entry(max=10)
        fentry_birth  = gtk.Entry(max=10)
        fentry_sex=gtk.combo_box_new_text()
        fentry_sex.append_text("Feminino")
        fentry_sex.append_text("Masculino")
        fentry_search = gtk.Entry(max=10)

        fentry_esco  = gtk.Entry(max=20)
        fentry_tel  = gtk.Entry(max=15)
        fentry_email  = gtk.Entry(max=50)
        fentry_addr  = gtk.Entry(max=300)
        fentry_cep  = gtk.Entry(max=10)

	
        fvbox.pack_start(flabel_name)
        fvbox2.pack_start(fentry_name)
        fvbox.pack_start(flabel_id)
        fvbox2.pack_start(fentry_id)
        fvbox.pack_start(flabel_sex)
        fvbox2.pack_start(fentry_sex)
        fvbox.pack_start(flabel_idade)
        fvbox2.pack_start(fentry_idade)
        fvbox.pack_start(flabel_birth)
        fvbox2.pack_start(fentry_birth)
        fvbox.pack_start(flabel_esco)
        fvbox2.pack_start(fentry_esco)

        fvbox3.pack_start(flabel_addr)
        fvbox4.pack_start(fentry_addr)
        fvbox3.pack_start(flabel_cep)
        fvbox4.pack_start(fentry_cep)
        fvbox3.pack_start(flabel_tel)
        fvbox4.pack_start(fentry_tel)
        fvbox3.pack_start(flabel_email)
        fvbox4.pack_start(fentry_email)

#       self.statusbar = gtk.Statusbar()
#       hbox.pack_start(self.statusbar,True,True,0)
#       self.context_id = self.statusbar.get_context_id("context_description")
#       self.statusbar.show()

        fbutton_add = gtk.Button(stock=gtk.STOCK_ADD)
        fbutton_clear = gtk.Button(stock=gtk.STOCK_CLEAR)
        fbutton_search = gtk.Button(stock=gtk.STOCK_FIND)
        fbutton_save = gtk.Button(stock=gtk.STOCK_SAVE)
        fvboxp.pack_start(fhbox7)
        fvboxp.pack_start(fhbox)
        fvboxp.pack_start(fhbox5)
        fvboxp.pack_start(fhbox6)

        fhbox.pack_start(fhbox2)
        fhbox2.pack_start(fframe)
        fhbox2.pack_start(fframe3)
        fhbox5.pack_start(fframe2)

        fhbox6.pack_start(fbutton_save)
        fhbox6.pack_start(fbutton_add)
        fhbox6.pack_start(fbutton_clear)

        fhbox7.pack_start(flabel_search)
        fhbox7.pack_start(fentry_search)
        fhbox7.pack_start(fbutton_search)

        fhbox3.pack_start(fvbox,False,False,5)
        fhbox3.pack_start(fvbox2)

        fhbox4.pack_start(fvbox3,False,False,50)
        fhbox4.pack_start(fvbox4)

        fframe.add(fhbox3)
        fframe2.add(fhbox4)

#########################################################################

	painel_frame = gtk.Frame("Controle")


	ptable = gtk.Table(2,8,False)
	painel_frame.add(ptable)
	pvbox = gtk.VBox(False, 5)
	pvbox2= gtk.VBox(False, 5)
	pvbox3= gtk.VBox(False, 5)
	pvbox4= gtk.VBox(False, 5)
	pvbox5= gtk.VBox(False, 5)
	pvbox6= gtk.VBox(False, 5)

	phbox = gtk.HBox(False, 1) 

	ptable.attach(pvbox,0,1,0,1)
	ptable.attach(pvbox2,1,2,0,1)
	ptable.attach(pvbox3,2,3,0,1)
	ptable.attach(pvbox4,4,5,0,1)
	ptable.attach(pvbox5,5,6,0,1)
	ptable.attach(pvbox6,6,7,0,1)
	ptable.set_col_spacing(1,20)
	
	for i in maquinas:
		label = gtk.Label(i[0])
        	pvbox.pack_start(label)
	for i in range(len(maquinas)):
		self.vars.append(gtk.Entry())
		self.vars[i].set_editable(editable=False)
#		self.vars.append(gtk.Label())
        	pvbox2.pack_start(self.vars[i])
	
	for i in range(len(maquinas)):
	        button = gtk.Button(stock="Adicionar 15 minutos")
		button.connect("clicked", self.add15,i)
        	pvbox3.pack_start(button)
	for i in range(len(maquinas)):
	        button = gtk.Button(stock="Adicionar 30 minutos")
		button.connect("clicked", self.add30,i)
        	pvbox4.pack_start(button)
	for i in range(len(maquinas)):
	        button = gtk.Button(stock="Adicionar 1 hora")
		button.connect("clicked", self.add60,i)
        	pvbox5.pack_start(button)
	for i in range(len(maquinas)):
	        button = gtk.Button(stock=gtk.STOCK_CANCEL)
		button.connect("clicked", self.cancelseasson, i)
        	pvbox6.pack_start(button)
	
	
	self.statusbar = gtk.Statusbar()
	phbox.pack_start(self.statusbar,True,True,0)
	self.context_id = self.statusbar.get_context_id("context_description")
	self.statusbar.show()
       	ptable.attach(phbox,0,7,7,8)
	mtable.attach(notebook,0,3,0,6)

	notebook.insert_page(painel_frame,gtk.Label("Painel"))
	notebook.insert_page(fvboxp,gtk.Label("Cadastro"))
	notebook.insert_page(gtk.Label("sdf"),gtk.Label("Configuração"))
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
    Painel()
#    EditBox()
    gtk.main()

if __name__ == '__main__':
    main()

