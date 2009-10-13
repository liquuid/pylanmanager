from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from pylan.controle.models import *
from forms import *
from django.core import serializers
import re
from time import time

def hello(request):
	return HttpResponse("uia")

def index(request):
	lista = Computadores.objects.all().order_by('nome')
	return render_to_response('computadores/index.html',locals())

def json(request):
	comp = Computadores.objects.all()
	for i in comp:
		i.remain = int(((i.dateIni+i.tempo) - time())/60)
	compz = serializers.serialize("json",comp)
	tempo = time()
	return HttpResponse(compz,mimetype="text/javascript")

def computadores(request,ip):
	comp = Computadores.objects.all().get(ip=ip)
	form = ControleForm(initial={'nome':comp.nome,'ip':comp.ip,'inicio':comp.dateIni,'tempo':comp.tempo}) 
	if request.method == 'POST':
		if form['nome']:
			print "nome ok"

		if form['ip']:
			print "ip ok"
		if form['tempo']:
			print "tempo ok"
		if form['dateIni']:
			print "date ok"
		if form.is_valid():
			form = ControleForm(request.POST)
			print form.cleaned_data['nome']	
			nome = form.cleaned_data['nome']
			ip= form.cleaned_data['ip']
			tempo=form.cleaned_data['tempo']			
			dateIni = form.cleaned_data['dateIni']
			c = Computadores()
	
			c.nome = re.sub('<.*?>','',nome)
			c.ip = re.sub('<.*?>','',ip)
			c.tempo = re.sub('<.*?>','',tempo)
			c.dateIni = re.sub('<.*?>','',dateIni)
			c.save()

			return render_to_response('refresh.html',locals())
		else:
			print "erro no form"

	return render_to_response('computadores/computadores.html',locals())

def ajax(request):
	if not request.POST:
		return render_to_response('computadores/ajax.html',locals())
	xhr = request.GET.has_key('xhr')
	response_dict={}
	name = request.POST.get('name',False)
	total = request.POST.get('total',False)
	response_dict.update({'name':name,'total':total})
	if total:
		try:
			total = int(total)
		except:
			total = False
	if name and total and int(total) == 10:
		response_dict.update({'succes': True })
	else:
		response_dict.update({'errors': {}})
		if not name:
			response_dict['errors'].update({'name':'This field is required'})
		if not total and total is not False:
			response_dict['errors'].update({'total':'This field is required'})
		elif int(total) != 10:
			response_dict['errors'].update({'total':'Incorrect total'})
	if xhr:
		return HttpResponse(simplejson.dumps(response_dict),mimetype='application/javascript') 
	return render_to_response('computadores/ajax.html',locals())
	
#def timesremain(request,ip):
#	lista = Computadores.objects.all().get(ip=ip)
#	return render_to_response('computadores/time.html',locals())

