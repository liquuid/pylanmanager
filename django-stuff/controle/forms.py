from pylan.controle.models import *
from django  import forms

class ControleForm(forms.Form):
	ip = forms.CharField()
	nome = forms.CharField()
	tempo = forms.IntegerField()
	dateIni = forms.IntegerField()

