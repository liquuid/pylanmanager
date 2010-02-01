#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import subprocess,os,urllib

def get_interface():
	arquivo = open('/etc/pylan-client.conf')
	configuracao = arquivo.read()
	arquivo.close()

	for i in configuracao.split():
	        if i.split('=')[0]=="interface":
	                return i.split('=')[1]
	print 'erro ao obter interface'

def get_serverip():
        arquivo = open('/etc/pylan-client.conf')
        configuracao = arquivo.read()
        arquivo.close()
	for i in configuracao.split():
	        if i.split('=')[0]=="server":
	                return i.split('=')[1]
	print 'erro ao obter o ip do servidor'

def get_ip():
	interface = get_interface()
	command = 'LANG=C /sbin/ifconfig '+interface+' | grep "inet add" | cut -d ":" -f 2| sed "s/ //g" | sed "s/Bcast//g" | sed "s/Mask//g"'
	proc = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
	os.waitpid(proc.pid,0)
	return proc.stdout.read().strip()


def get_workdir():
	try:
	        arquivo = open('/etc/pyland.conf','r')
	except:
	        print 'arquivo de configuração não encontrado (/etc/pyland.conf)'
	        exit()

	afd = arquivo.read()
	arquivo.close()
	workdir = afd.split('=')[1].strip()

	try:
	        os.mkdir(workdir)
	except:
	        print 'Erro ao criar diretório de trabalho (já existe ?)'

	return workdir
	
