# _*_ coding: UTF-8 _*_
from django.db import models
from datetime import datetime
from time import time
class Computadores(models.Model):
	ip = models.CharField(max_length=50)
	nome = models.CharField(max_length=100)
	tempo = models.IntegerField()
	dateIni = models.IntegerField()

	def unixInitoDatetime(self):
		return datetime.fromtimestamp(self.dateIni)
	def secTominute(self):
		return self.tempo/60
	def timeRemain(self):
		return int(((self.dateIni+self.tempo) - time())/60) 
	
	def __unicode__(self):
		return self.nome
