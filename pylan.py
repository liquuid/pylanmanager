#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import gobject
import gtk
from datetime import datetime
from time import time
import sys
import os

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
	print 'erro ao criar diretório de cache'


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
	
	for i in maquinas:
		label = gtk.Label(i[0])
        	vbox.pack_start(label)
	for i in range(len(maquinas)):
		self.vars.append(gtk.Entry())
        	vbox2.pack_start(self.vars[i])
	
	for i in range(len(maquinas)):
	        button = gtk.Button(stock="Adicionar 15 minutos")
		button.connect("clicked", self.add15,i)
        	vbox3.pack_start(button)
	for i in range(len(maquinas)):
	        button = gtk.Button(stock="Adicionar 30 minutos")
		button.connect("clicked", self.add30,i)
        	vbox4.pack_start(button)
	for i in range(len(maquinas)):
	        button = gtk.Button(stock="Adicionar 1 hora")
		button.connect("clicked", self.add60,i)
        	vbox5.pack_start(button)
	for i in range(len(maquinas)):
	        button = gtk.Button(stock=gtk.STOCK_CANCEL)
		button.connect("clicked", self.cancelseasson, i)
        	vbox6.pack_start(button)
	
	
	self.statusbar = gtk.Statusbar()
	hbox.pack_start(self.statusbar,True,True,0)
	self.context_id = self.statusbar.get_context_id("context_description")
	self.statusbar.show()
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
    Painel()
#    EditBox()
    gtk.main()

if __name__ == '__main__':
    main()

