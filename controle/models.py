# _*_ coding: UTF-8 _*_
from django.db import models

class Computadores(models.Model):
	ip = models.CharField(max_length=50)
	nome = models.CharField(max_length=100)
	dateIni = models.TimeField()
	dateTer = models.TimeField()
