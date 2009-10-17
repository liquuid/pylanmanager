#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import gobject
import gtk
from datetime import datetime

#   columns
(
  COLUMN_NAME,
  COLUMN_START,
  COLUMN_TIME,
  COLUMN_REMAIN,
  COLUMN_IP,
  COLUMN_EDITABLE
) = range(6)

# data
listas = [
		[ "pc01", "12:12",1,0,"192.168.0.101", True ],
		[ "pc02", "12:12",2,0,"192.168.0.102", True ],
		[ "pc03", "13:13",3,0,"192.168.0.103", True ],
		[ "pc04", "14:14",4,0,"192.168.0.104", True ],
		[ "pc05", "15:15",5,0,"192.168.0.105", True ]
]



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
	hbox = gtk.HBox(False,1) 

	table.attach(vbox,0,1,0,1)
	table.attach(vbox2,1,2,0,1)
	table.attach(vbox3,2,3,0,1)
	table.attach(vbox4,4,5,0,1)
	table.attach(vbox5,5,6,0,1)
	table.set_col_spacing(1,20)
	
	for i in listas:
		label = gtk.Label(i[0])
        	vbox.pack_start(label)
	for i in range(len(listas)):
		self.vars.append(gtk.Entry())
        	vbox2.pack_start(self.vars[i])
	
	for i in listas:
	        button = gtk.Button(stock="Adicionar 15 minutos")
		button.connect("clicked", self.on_add_item_clicked, None)
        	vbox3.pack_start(button)
	for i in listas:
	        button = gtk.Button(stock="Adicionar 30 minutos")
		button.connect("clicked", self.on_add_item_clicked, None)
        	vbox4.pack_start(button)
	for i in listas:
	        button = gtk.Button(stock="Adicionar 1 hora")
		button.connect("clicked", self.on_add_item_clicked, None)
        	vbox5.pack_start(button)

	
	self.statusbar = gtk.Statusbar()
	hbox.pack_start(self.statusbar,True,True,0)
	self.context_id = self.statusbar.get_context_id("context_description")
	#self.statusbar.push(self.context_id,"text")
	#statusbar.pop(context_id)
	self.statusbar.show()
       	table.attach(hbox,0,6,7,8)

	self.show_all()

    def __showvars(self,button,model):
	while 1:
		while gtk.events_pending():gtk.main_iteration()
		print datetime.now()


    def on_add_item_clicked(self, button, model):
	print listas
	new_item = ["pc", "00:00",0,0,"192.168.0.0", True]
        listas.append(new_item)

        iter = model.append()
        model.set (iter,
            COLUMN_NAME, new_item[COLUMN_NAME],
            COLUMN_START, new_item[COLUMN_START],
	    COLUMN_TIME, new_item[COLUMN_TIME],
	    COLUMN_REMAIN, new_item[COLUMN_REMAIN],
	    COLUMN_IP, new_item[COLUMN_IP],
            COLUMN_EDITABLE, new_item[COLUMN_EDITABLE]
       )


def tempo(self):
	for i in range(len(self.vars)):
		self.vars[i].set_text(str(datetime.now())) 
	self.statusbar.push(self.context_id,str(datetime.now()))
	return True


def main():
    Painel()
    gtk.main()

if __name__ == '__main__':
    main()

