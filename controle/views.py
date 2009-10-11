from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from pylan.controle.models import *
def hello(request):
	return HttpResponse("uia")

def index(request):
	lista = Computadores.objects.all().order_by('nome')
	return render_to_response('computadores/index.html',locals())
#def timesremain(request,ip):
#	lista = Computadores.objects.all().get(ip=ip)
#	return render_to_response('computadores/time.html',locals())

