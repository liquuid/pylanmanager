#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import gobject
import gtk
from datetime import datetime
from time import time
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
		[ "pc01",1255926026, 10,0,"192.168.0.101", True ],
		[ "pc02",1255926026, 20,0,"192.168.0.102", True ],
		[ "pc03",1255926000, 30,0,"192.168.0.103", True ],
		[ "pc04",1255925000, 40,0,"192.168.0.104", True ],
		[ "pc05",1255924000, 50,0,"192.168.0.105", True ]
		]



class EditBox(gtk.Window):
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
	button.connect("clicked",self.__showvars,None)
	hbox.pack_start(button)

	self.statusbar = gtk.Statusbar()
	vbox.pack_start(self.statusbar,False,True,0)
	self.statusbar.show()
	self.context_id = self.statusbar.get_context_id("context_description")
	#self.statusbar.push(self.context_id,"text")
	#statusbar.pop(context_id)

        self.show_all()

    def __showvars(self,button,model):
	while 1:
		while gtk.events_pending():gtk.main_iteration()
		print datetime.now()

    def __create_model(self):

        # create list store
        model = gtk.ListStore(
            gobject.TYPE_STRING,
            gobject.TYPE_STRING,
	    gobject.TYPE_INT,
	    gobject.TYPE_INT,
	    gobject.TYPE_STRING,
            gobject.TYPE_BOOLEAN
       )

        # add items
        for item in listas:
            iter = model.append()

            model.set (iter,
                  COLUMN_NAME, item[COLUMN_NAME],
                  COLUMN_START, item[COLUMN_START],
		  COLUMN_TIME,item[COLUMN_TIME],
		  COLUMN_REMAIN, item[COLUMN_REMAIN],
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

        # remain column
        renderer = gtk.CellRendererText()
        renderer.connect("edited", self.on_cell_edited, model)
        renderer.set_data("column", COLUMN_REMAIN)

        column = gtk.TreeViewColumn("Restante", renderer, text=COLUMN_REMAIN,
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
	print listas
	new_item = ["pc", int(time()),0,0,"192.168.0.0", True]
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


    def on_remove_item_clicked(self, button, treeview):

        selection = treeview.get_selection()
        model, iter = selection.get_selected()

        if iter:
            path = model.get_path(iter)[0]
            model.remove(iter)

            del listas[ path ]


    def on_cell_edited(self, cell, path_string, new_text, model):

        iter = model.get_iter_from_string(path_string)
        path = model.get_path(iter)[0]
        column = cell.get_data("column")

        if column == COLUMN_NAME:
            listas[path][COLUMN_NAME] = new_text

            model.set(iter, column, listas[path][COLUMN_NAME])

        elif column == COLUMN_START:
            old_text = model.get_value(iter, column)
            listas[path][COLUMN_START] = int(new_text)

            model.set(iter, column, listas[path][COLUMN_START])
    	elif column == COLUMN_TIME:
		old_text = model.get_value(iter,column)
		listas[path][COLUMN_TIME] = int(new_text)

		model.set(iter,column, listas[path][COLUMN_TIME])
    	elif column == COLUMN_REMAIN:
		old_text = model.get_value(iter,column)
		listas[path][COLUMN_REMAIN] = int(new_text)

		model.set(iter,column, listas[path][COLUMN_REMAIN])
    	elif column == COLUMN_IP:
		old_text = model.get_value(iter,column)
		listas[path][COLUMN_IP] = new_text

		model.set(iter,column, listas[path][COLUMN_IP])

def tempo(self):

	self.statusbar.push(self.context_id,str(datetime.now()))
	return True


def main():
    EditBox()
    gtk.main()

if __name__ == '__main__':
    main()

