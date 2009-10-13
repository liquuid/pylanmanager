# _*_ coding: UTF-8 _*_
from django.db import models
from datetime import datetime
from time import time
class Computadores(models.Model):
	nome = models.CharField(max_length=100)
	ip = models.CharField(max_length=50)
	remain = models.IntegerField()
	tempo = models.IntegerField()
	coments = models.CharField(max_length=100)
	dateIni = models.IntegerField()

	def unixInitoDatetime(self):
		return datetime.fromtimestamp(self.dateIni)
	def secTominute(self):
		return self.tempo/60
	def timeRemain(self):
		remain = int(((self.dateIni+self.tempo) - time())/60) 
		if remain <= 0:
			return "liberado"
		else:
			return remain
	def __unicode__(self):
		return self.nome
