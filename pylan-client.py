import urllib, time, os

while 1:
	h = urllib.urlopen('http://localhost:8000/192.168.0.1')
	tempo = h.read()
	tempo = tempo.strip()
	if int(tempo) > 0:
		print tempo
	else:
		print "tempo acabou"
		os.system('killall -9 xterm')

	time.sleep(1)
