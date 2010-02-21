#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import pylan
import pylanrc
import time

workdir = pylanrc.get_workdir()

class TestClients:
	def __init__(self,numtest,time):
		self.numtest = numtest
		self.time = time
	def print_args(self):
		print self.numtest
		print self.time
	def run_sessions(self):
		for seasson in xrange(self.numtest):
			print "#"*10+" Teste numero: "+str(seasson+1)+" "+"#"*10
			for i in xrange(int(self.time)*60): 		
				for j in pylan.maquinas:
					fd = open(workdir+j[3],'w')
					fd.write(str((self.time*60)-i-1))
					fd.close()
					print workdir+j[3]+" "+sec2beauty((self.time*60)-i-1)
				time.sleep(1)	

def sec2beauty(hud):
        hor = str(hud/3600)
        min = str((hud%3600)/60)
        seg = str((hud%3600)%60)
        hud = str(n(hor)+':'+n(min)+':'+n(seg))
	
	return hud

def n(var):
        """ Recebe um número com um digito e retorna o mesmo numero com um zero na frente """
        if len(var) < 2:
                return '0'+var
        else:
                return var




def main():
	w = TestClients(3,1)
	w.run_sessions()

if __name__ == '__main__':
	main()
