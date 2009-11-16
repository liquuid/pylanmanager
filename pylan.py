#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import gobject
import gtk
from datetime import datetime
from time import time
import sys
import os
import sqlite3

columns=8
ciclo = 1

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
	# Cria as tabelas
	cur.execute('CREATE TABLE users(id INTEGER PRIMARY KEY,name VARCHAR,gender NUMBER,birthday VARCHAR,grad NUMBER,address VARCHAR,zip VARCHAR,phone VARCHAR,email VARCHAR)')
	cur.execute('CREATE TABLE log(id INTEGER PRIMARY KEY,username VARCHAR,userid INTEGER,computer VARCHAR,ip VARCHAR,date VARCHAR,min INTEGER)')
	# Preenche a tabela users com exemplos
	cur.execute('insert into users (id,name,gender,birthday,grad,address,zip,phone,email) VALUES(123456789,\'João José da Silva\',1,\'11/08/1978\',1,\'Rua da esquina num\',\'06626-080\',\'5555-1111\',\'jaum@example.com\');')
	cur.execute('insert into users (id,name,gender,birthday,grad,address,zip,phone,email) VALUES(234567890,\'Jeniuma Souza Santos\',0,\'22/04/1991\',4,\'Rua das Flores,123 \',\'1234-1236\',\'12334-123\',\'tesy@example.com\');')
	connection.commit()
	
connection = sqlite3.connect(os.path.expanduser('~/')+'.pylandb.sqlite3')
cur = connection.cursor()

maquinas=[]
list_conf=[]

config = open(os.path.expanduser('~/')+'.pylanrc','r')
cfd = config.read()

for i in range(len(cfd.split('\n'))):
	if cfd.split('\n')[i]:
		maquinas.append([cfd.split('\n')[i].split(',')[0],0,0,cfd.split('\n')[i].split(',')[1],0,'',True])
		list_conf.append([cfd.split('\n')[i].split(',')[0],cfd.split('\n')[i].split(',')[1],True])

config.close()

#   columns
(
  COLUMN_NAME,
  COLUMN_IP,
  COLUMN_EDITABLE
) = range(3)

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
	self.nomes = []
	self.box_matrix=[]
	self.box_line=[] 
	self.lista_controle = []
	notebook = gtk.Notebook()
	notebook.set_tab_pos(gtk.POS_TOP)
	
	mtable = gtk.Table(3,6,False)
	self.add(mtable)


###############################################################################
# Aba de logs

	log_frame = gtk.Frame("Histórico de acessos")

###############################################################################
# Aba de estatísticas 
	
	stat_frame = gtk.Frame("Estatísticas")

###############################################################################
#

###############################################################################
#

###############################################################################
# Aba de configurações

	config_frame = gtk.Frame("Configuração")

	edit_vbox = gtk.VBox(False, 5)
        config_frame.add(edit_vbox)

        label = gtk.Label("Lista de máquinas (editavel)")
        edit_vbox.pack_start(label, False, False)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        edit_vbox.pack_start(sw)

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
        edit_vbox.pack_start(hbox, False, False)

        button = gtk.Button(stock=gtk.STOCK_ADD)
        button.connect("clicked", self.on_add_item_clicked, model)
        hbox.pack_start(button)

        button = gtk.Button(stock=gtk.STOCK_REMOVE)
        button.connect("clicked", self.on_remove_item_clicked, treeview)
        hbox.pack_start(button)
	button = gtk.Button(stock=gtk.STOCK_REFRESH)
	button.connect("clicked",self.__showvars)
	hbox.pack_start(button)

	self.statusbar = gtk.Statusbar()
	edit_vbox.pack_start(self.statusbar,False,True,0)
	self.statusbar.show()
	self.context_id = self.statusbar.get_context_id("context_description")

 

########################################################################
# Código para criar as boxes para o controle a partir do formulario
	fcontrolebox = gtk.VBox(False,1)

	for i in xrange((len(maquinas)/columns)+1):
		self.box_line.append(gtk.HBox(False,5))
	for i in xrange(len(self.box_line)):
		fcontrolebox.pack_start(self.box_line[i])

########################################################################
# Painel de cadastro de usuários

        box_id_esquerdo = gtk.VBox(True, 5)
        frame_form_root= gtk.VBox(False, 5)
        box_id_direito= gtk.VBox(False, 5)
        box_contato_esquerdo= gtk.VBox(False, 5)
        box_contato_direito= gtk.VBox(False, 5)

        fhbox = gtk.HBox(False, 1)
        fhbox2 = gtk.HBox(False,1)
        fhbox3 = gtk.HBox(False,1)
        fhbox4 = gtk.HBox(False,1)
        fhbox5 = gtk.HBox(False,1)
        fhbox6 = gtk.HBox(False,1)
        fhbox7 = gtk.HBox(False,1)

#	fcontrolebox = gtk.HBox(False,1)

        frame_id= gtk.Frame('Identificação')
        frame_contato= gtk.Frame('Contato')
	frame_controle = gtk.Frame('Iniciar sessão no computador :')
        fframe4 = gtk.Frame('Busca')

        flabel_name = gtk.Label("Nome")
        flabel_birth = gtk.Label("Data de Nascimento (dd/mm/aaaa)")
        flabel_sex = gtk.Label("Sexo")
        flabel_id = gtk.Label("RG")
        flabel_esco = gtk.Label("Escolaridade")
        flabel_tel = gtk.Label("Telefone")
        flabel_email = gtk.Label("Email")
        flabel_addr = gtk.Label("Endereço")
        flabel_cep = gtk.Label("CEP")
        flabel_search = gtk.Label("Buscar ")
        flabel_name.set_justify(gtk.JUSTIFY_RIGHT)
        flabel_name.set_justify(gtk.JUSTIFY_RIGHT)

        self.fentry_name  = gtk.Entry()
        self.fentry_id = gtk.Entry(max=15)
        self.fentry_birth  = gtk.Entry(max=10)
        self.fentry_sex=gtk.combo_box_new_text()
        self.fentry_sex.append_text("Feminino")
        self.fentry_sex.append_text("Masculino")
        self.fentry_search = gtk.Entry()
	

        self.fentry_esco  = gtk.combo_box_new_text()
	self.fentry_esco.append_text("Ensino fundamental incompleto")
	self.fentry_esco.append_text("Ensino fundamental")
      	self.fentry_esco.append_text("Ensino médio incompleto")
	self.fentry_esco.append_text("Ensino médio")
	self.fentry_esco.append_text("Ensino superior incompleto")
	self.fentry_esco.append_text("Ensino superior")
	self.fentry_tel  = gtk.Entry(max=15)
        self.fentry_email  = gtk.Entry(max=50)
        self.fentry_addr  = gtk.Entry(max=300)
        self.fentry_cep  = gtk.Entry(max=10)

	self.fentry_type_search = gtk.combo_box_new_text()
	self.fentry_type_search.append_text('por nome')
	self.fentry_type_search.append_text('por RG')
	self.fentry_type_search.set_active(0)

#	completion = gtk.EntryCompletion()
#	self.fentry_search.set_completion(completion)
#       completion_model = self.__create_completion_model()
#       completion.set_model(completion_model)
#       print completion
#       # Use model column 0 as the text column
#       completion.set_text_column(0)



        box_id_esquerdo.pack_start(flabel_name)
        box_id_direito.pack_start(self.fentry_name)
        box_id_esquerdo.pack_start(flabel_id)
        box_id_direito.pack_start(self.fentry_id)
        box_id_esquerdo.pack_start(flabel_sex)
        box_id_direito.pack_start(self.fentry_sex)
        box_id_esquerdo.pack_start(flabel_birth)
        box_id_direito.pack_start(self.fentry_birth)
        box_id_esquerdo.pack_start(flabel_esco)
        box_id_direito.pack_start(self.fentry_esco)

        box_contato_esquerdo.pack_start(flabel_addr)
        box_contato_direito.pack_start(self.fentry_addr)
        box_contato_esquerdo.pack_start(flabel_cep)
        box_contato_direito.pack_start(self.fentry_cep)
        box_contato_esquerdo.pack_start(flabel_tel)
        box_contato_direito.pack_start(self.fentry_tel)
        box_contato_esquerdo.pack_start(flabel_email)
        box_contato_direito.pack_start(self.fentry_email)

#       self.statusbar = gtk.Statusbar()
#       hbox.pack_start(self.statusbar,True,True,0)
#       self.context_id = self.statusbar.get_context_id("context_description")
#       self.statusbar.show()

        fbutton_add = gtk.Button(stock=gtk.STOCK_ADD)
        fbutton_clear = gtk.Button(stock=gtk.STOCK_CLEAR)
        fbutton_search = gtk.Button(stock=gtk.STOCK_FIND)
        fbutton_save = gtk.Button(stock=gtk.STOCK_SAVE)
       	 
	fbutton_search.connect('clicked',self.search_pressed)
	fbutton_clear.connect('clicked',self.clear_pressed)
	fbutton_add.connect('clicked',self.add_pressed)
	fbutton_save.connect('clicked',self.save_pressed)

	frame_form_root.pack_start(fhbox7)
        frame_form_root.pack_start(fhbox)
        frame_form_root.pack_start(fhbox5)
        frame_form_root.pack_start(fhbox6)

        fhbox.pack_start(fhbox2)
        fhbox2.pack_start(frame_id)
        fhbox2.pack_start(frame_controle)
        fhbox5.pack_start(frame_contato)

        fhbox6.pack_start(fbutton_save)
        fhbox6.pack_start(fbutton_add)
        fhbox6.pack_start(fbutton_clear)

        fhbox7.pack_start(flabel_search)
        fhbox7.pack_start(self.fentry_search)
	fhbox7.pack_start(self.fentry_type_search)
        fhbox7.pack_start(fbutton_search)

        fhbox3.pack_start(box_id_esquerdo,False,False,5)
        fhbox3.pack_start(box_id_direito)

        fhbox4.pack_start(box_contato_esquerdo,False,False,50)
        fhbox4.pack_start(box_contato_direito)

        frame_id.add(fhbox3)
        frame_contato.add(fhbox4)
	frame_controle.add(fcontrolebox)
	count = 0
	for i in maquinas:
		self.lista_controle.append(gtk.ToggleButton(i[0]))
		self.lista_controle[count].connect("clicked", self.addciclo,count,self.fentry_id,self.fentry_name)
		self.box_line[count/columns].pack_start(self.lista_controle[count])
		count = count + 1


#########################################################################
# Painel de controle das máquinas

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
        	pvbox2.pack_start(label)
	for i in range(len(maquinas)):
		self.vars.append(gtk.Entry())
		self.vars[i].set_editable(editable=False)
#		self.vars.append(gtk.Label())
        	pvbox3.pack_start(self.vars[i])
	for i in range(len(maquinas)):
		self.nomes.append(gtk.Label())
        	pvbox.pack_start(self.nomes[i])
	for i in range(len(maquinas)):
	        button = gtk.Button(stock="Adicionar "+str(1)+" minutos")
		button.connect("clicked", self.add30,i)
        	pvbox4.pack_start(button)
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
	notebook.insert_page(frame_form_root,gtk.Label("Cadastro"))
	notebook.insert_page(config_frame,gtk.Label("Configuração"))
	notebook.insert_page(log_frame,gtk.Label("Histórico"))
	notebook.insert_page(stat_frame,gtk.Label("Estatísticas"))

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


    def add30(self,button,i):
	if self.timeout(i):
		maquinas[i][1] = int(time())
		maquinas[i][2] = ciclo
	else:
		maquinas[i][2] = maquinas[i][2] + ciclo

    def addciclo(self,button,i,id,nome):
	id = int(cleanup_id(id.get_text()))
	if not allreadyin(self,id):
		i = int(i)
		nome = nome.get_text()
		maquinas[i][4]=id
		maquinas[i][5]=nome
		if self.timeout(i):
			maquinas[i][1] = int(time())
			maquinas[i][2] = ciclo
			print maquinas[i]

			cur.execute('INSERT INTO log (username,userid,computer,ip,date,min) values(\''+str(maquinas[i][5])+'\','+str(id)+',\''+maquinas[i][0]+'\',\''+maquinas[i][3]+'\',\''+str(datetime.now())+'\','+str(maquinas[i][2])+');')
			connection.commit()
		else:
			maquinas[i][2] = maquinas[i][2] + ciclo

    def search_pressed(self,button):
	type = self.fentry_type_search.get_active()
	parametro = self.fentry_search.get_text().replace('.','').replace('-','').replace(' ','%').replace('\'','')
	if type == 0:
		dados = search_by_name(self,parametro)[0]
	else:
		dados = search_by_id(self,parametro)[0]
	
	id = str(dados[0])
	if len(str(id)) == 9:
		id = id[0:2]+'.'+id[2:5]+'.'+id[5:8]+'-'+id[8]
	
	self.fentry_id.set_text(id)
	self.fentry_name.set_text(str(dados[1]))
	self.fentry_birth.set_text(str(dados[3]))
	self.fentry_addr.set_text(str(dados[5]))
	self.fentry_cep.set_text(str(dados[6]))
	self.fentry_tel.set_text(str(dados[7]))
	self.fentry_email.set_text(str(dados[8]))
	self.fentry_esco.set_active(dados[4])
	self.fentry_sex.set_active(dados[2])
	
    def clear_pressed(self,button):
	    clear_fields(self)

    def add_pressed(self,button):
	    update_fields(self)
	    clear_fields(self)
    def save_pressed(self,button):
	    update_fields(self)

    def __create_model(self):

        # create list store
        model = gtk.ListStore(
            gobject.TYPE_STRING,
	    gobject.TYPE_STRING,
            gobject.TYPE_BOOLEAN
       )

        # add items
        for item in list_conf:
            iter = model.append()

            model.set (iter,
                  COLUMN_NAME, item[COLUMN_NAME],
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


        # ip column
        renderer = gtk.CellRendererText()
        renderer.connect("edited", self.on_cell_edited, model)
        renderer.set_data("column", COLUMN_IP)

        column = gtk.TreeViewColumn("IP", renderer, text=COLUMN_IP,
                               editable=COLUMN_EDITABLE)
        treeview.append_column(column)


    def on_add_item_clicked(self, button, model):
	new_item = ["pc","192.168.0.0", False]
        list_conf.append(new_item)

        iter = model.append()
        model.set (iter,
            COLUMN_NAME, new_item[COLUMN_NAME],
	    COLUMN_IP, new_item[COLUMN_IP],
            COLUMN_EDITABLE, new_item[COLUMN_EDITABLE]
       )


    def on_remove_item_clicked(self, button, treeview):

        selection = treeview.get_selection()
        model, iter = selection.get_selected()

        if iter:
            path = model.get_path(iter)[0]
            model.remove(iter)

            del list_conf[ path ]


    def on_cell_edited(self, cell, path_string, new_text, model):

        iter = model.get_iter_from_string(path_string)
        path = model.get_path(iter)[0]
        column = cell.get_data("column")

        if column == COLUMN_NAME:
            list_conf[path][COLUMN_NAME] = new_text

            model.set(iter, column, list_conf[path][COLUMN_NAME])
    	elif column == COLUMN_IP:
		old_text = model.get_value(iter,column)
		list_conf[path][COLUMN_IP] = new_text

		model.set(iter,column, list_conf[path][COLUMN_IP])

#    def __create_completion_model(self):
#	        ''' Creates a tree model containing the completions.
#	        '''
#	        store = gtk.ListStore(str)
#
#	        cur.execute('select name from users;')
#		resu = cur.fetchall()
#	
#		for i in resu:
#			print i
#		        iter = store.append()
#		        store.set(iter, 0,str(i))
#		print store
#	        return store


def cleanup_id(string):
	return string.replace('.','').replace('-','')


def update_fields(self):
	if self.fentry_id.get_text():
		print '$'*80
		print 'replace into users (id,name,gender,birthday,grad,address,zip,phone,email) VALUES('+str(self.fentry_id.get_text().replace('.','').replace('-',''))+','+self.fentry_name.get_text()+','+str(self.fentry_sex.get_active())+','+self.fentry_birth.get_text()+','+str(self.fentry_esco.get_active())+','+self.fentry_addr.get_text()+','+self.fentry_cep.get_text()+','+self.fentry_tel.get_text()+','+self.fentry_email.get_text()+');'
		print '$'*80

		cur.execute('replace into users (id,name,gender,birthday,grad,address,zip,phone,email) VALUES('+str(self.fentry_id.get_text().replace('.','').replace('-',''))+',"'+self.fentry_name.get_text()+'",'+str(self.fentry_sex.get_active())+',"'+self.fentry_birth.get_text()+'",'+str(self.fentry_esco.get_active())+',"'+self.fentry_addr.get_text()+'","'+self.fentry_cep.get_text()+'","'+self.fentry_tel.get_text()+'","'+self.fentry_email.get_text()+'");')
		connection.commit()

def clear_fields(self):
	self.fentry_id.set_text(str(''))
	self.fentry_name.set_text(str(''))
	self.fentry_birth.set_text(str(''))
	self.fentry_addr.set_text(str(''))
	self.fentry_cep.set_text(str(''))
	self.fentry_tel.set_text(str(''))
	self.fentry_email.set_text(str(''))
	self.fentry_id.set_text(str(''))
	self.fentry_id.set_text(str(''))
	self.fentry_sex.set_active(-1)
	self.fentry_esco.set_active(-1)

def search_by_id(self,id):
	cur.execute('select * from users where id=\''+id+'\';')
	return cur.fetchall()

def search_by_name(self,string):
	cur.execute('select * from users where name like \'%'+string+'%\';')
	return cur.fetchall()


def allreadyin(self,id):
	for i in xrange(len(maquinas)):
		if int(id) == int(maquinas[i][4]):
			for j in xrange(len(maquinas)):
				self.lista_controle[j].set_sensitive(False)
			self.lista_controle[i].set_active(True)
			return True
	return False

def tempo(self):
	for i in range(len(self.vars)):
		if self.timeout(i):
			self.lista_controle[i].set_sensitive(True)
		else:
			self.lista_controle[i].set_sensitive(False)

		fid = self.fentry_id.get_text()
		if fid == str(maquinas[i][4]):
			for j in xrange(len(maquinas)):
				self.lista_controle[j].set_active(False)
				self.lista_controle[j].set_sensitive(True)
			self.lista_controle[i].set_active(True)

		if (int(maquinas[i][1])+int(maquinas[i][2]*60)-int(time()))/60.0 < 1 and (int(maquinas[i][1])+int(maquinas[i][2]*60)-int(time()))/60.0 > 0:
			self.vars[i].set_text(str((int(maquinas[i][1])+int(maquinas[i][2]*60)-int(time())))+" segundos")
			self.nomes[i].set_text(str(maquinas[i][5]))
		elif	self.timeout(i):
			self.vars[i].set_text(str("Disponível"))
			maquinas[i][4]=0
			maquinas[i][5]=''
			self.nomes[i].set_text(str(maquinas[i][5]))
			fd = open(os.path.expanduser('~/')+'.pyland/'+maquinas[i][3],'w')
			fd.write(str(0))
			fd.close()


                elif    not self.timeout(i):
                        self.vars[i].set_text(str((int(maquinas[i][1])+int(maquinas[i][2]*60)-int(time())+60)/60)+" minutos")
                        self.nomes[i].set_text(str(maquinas[i][5]))

                if not self.timeout(i):
                        fd = open(os.path.expanduser('~/')+'.pyland/'+maquinas[i][3],'w')
                        fd.write(str(int(maquinas[i][1])+int(maquinas[i][2]*60)-int(time())))
                        fd.close()


        self.statusbar.push(self.context_id,str(datetime.now()))
        return True


def fake():
	return True

def main():
    Painel()
    gtk.main()

if __name__ == '__main__':
    main()

