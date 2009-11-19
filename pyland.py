#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import SimpleHTTPServer
import os

try:
	arquivo = open('/etc/pyland.conf','r')
except:
	print 'arquivo de configuração não encontrado'
	exit()


afd = arquivo.read()
arquivo.close()
workdir = afd.split('=')[1].strip()

try:
	os.mkdir(workdir)
except:
	print 'Erro ao criar diretório de trabalho (já existe ?)'

os.chdir(workdir) 
SimpleHTTPServer.test()
