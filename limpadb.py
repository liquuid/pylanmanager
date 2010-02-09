#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import sqlite3
import os
connection = sqlite3.connect(os.path.expanduser('~/')+'.pylandb.sqlite3')
cur = connection.cursor()
# cur.execute('CREATE TABLE users(id INTEGER PRIMARY KEY,name VARCHAR,gender NUMBER,birthday VARCHAR,grad NUMBER,address VARCHAR,zip VARCHAR,phone VARCHAR,email VARCHAR)')
cur.execute('SELECT id FROM users;')
list = cur.fetchall()

for i in  list:
	cur.execute('SELECT * FROM users where id="'+str(i[0])+'";')
	resu = cur.fetchall()[0]
	for j in xrange(9):
		try:
			if str(resu[j]).count(',') > 0:
				if j == 5:
					cur.execute('replace into users (id,address) values("'+str(resu[0])+'","'+resu[j].replace(',','%')+'")')
					print resu[j]
				elif j == 8:
					cur.execute("replace into users (id,email) values('"+str(resu[0])+"','"+resu[j].replace(',','')+"')")
					print resu[j]

		except UnicodeEncodeError:
				#print resu
				pass
	if resu[3] and len(resu[3]) < 10:
		print "@"+resu[3]

	if resu[3] and len(resu[3]) < 10:
		bd = resu[3].replace('.','/')	
		bd =bd.replace('jan','01').replace('fev','02').replace('mar','03').replace('abr','04').replace('mai','05').replace('jun','06').replace('jul','07').replace('ago','08').replace('set','09').replace('out','10').replace('nov','11').replace('dez','12')
		bdt = bd.split('/')		
		
		if len(bdt) == 3 and bdt[2] == '':
			continue

		if len(bdt) == 3 and bdt[2] != '':
			if len(bdt[1]) == 3:
				bdt[1] = bdt[1][0:2]			
				print bdt[1]

			if len(bdt[2]) == 2:
				bdt[2]= "19"+str(bdt[2])
		
			if len(bdt[0]) < 2:
				bdt[0]= "0"+str(bdt[0])
			if len(bdt[1]) < 2:
				bdt[1] = '0'+bdt[1]
			if int(bdt[0]) > 31:
				bdt[0] = "01"
			if len(bdt[2]) == 3:
				if int(bdt[2]) > 110 and int(bdt[2]) < 200:
					bdt[2] = "19"+bdt[2][1:3]
					
					  
			bd = bdt[0]+'/'+bdt[1]+'/'+bdt[2]
		
			if bd.count('/') == 0 and len(bd) == 8:
				bd = str(bd[0:2])+'/'+str(bd[2:4])+'/'+bd[4:10]
		if len(bdt) == 2:
			if len(bdt[1]) == 6:
				bd = str(bdt[0])+'/'+bdt[1][0:2]+'/'+bdt[1][2:6]
			if len(bdt[0]) == 4:
				bd = str(bdt[0][0:2])+'/'+bdt[0][2:4]+'/'+bdt[1]
				print "--"+bd

		if len(bdt) == 1:
			bd = str(bdt[0][0:2])+'/'+str(bdt[0][2:4])+'/'+bdt[0][4:10]

		if len(bd) == 10:
			cur.execute('replace into users (id,birthday) values("'+str(resu[0])+'","'+bd+'")')
			print resu[0],bd
	
	if resu[3] and len(resu[3]) < 10 :
		print resu[3]	
cur.execute('SELECT id FROM log;')
list = cur.fetchall()

for i in  list:
	cur.execute('SELECT * FROM log where id="'+str(i[0])+'";')

	resu = cur.fetchall()[0]
	if resu[7] and len(resu[7]) < 10:
		print "@"+resu[7]

	if resu[7] and len(resu[7]) < 10:
		bd = resu[7].replace('.','/')	
		bd =bd.replace('jan','01').replace('fev','02').replace('mar','03').replace('abr','04').replace('mai','05').replace('jun','06').replace('jul','07').replace('ago','08').replace('set','09').replace('out','10').replace('nov','11').replace('dez','12')
		bdt = bd.split('/')		
		
		if len(bdt) == 3 and bdt[2] == '':
			continue

		if len(bdt) == 3 and bdt[2] != '':
			if len(bdt[1]) == 3:
				bdt[1] = bdt[1][0:2]			
				print bdt[1]

			if len(bdt[2]) == 2:
				bdt[2]= "19"+str(bdt[2])
		
			if len(bdt[0]) < 2:
				bdt[0]= "0"+str(bdt[0])
			if len(bdt[1]) < 2:
				bdt[1] = '0'+bdt[1]
			if int(bdt[0]) > 31:
				bdt[0] = "01"
			if len(bdt[2]) == 3:
				if int(bdt[2]) > 110 and int(bdt[2]) < 200:
					bdt[2] = "19"+bdt[2][1:3]
					
					  
			bd = bdt[0]+'/'+bdt[1]+'/'+bdt[2]
		
			if bd.count('/') == 0 and len(bd) == 8:
				bd = str(bd[0:2])+'/'+str(bd[2:4])+'/'+bd[4:10]
		if len(bdt) == 2:
			if len(bdt[1]) == 6:
				bd = str(bdt[0])+'/'+bdt[1][0:2]+'/'+bdt[1][2:6]
			if len(bdt[0]) == 4:
				bd = str(bdt[0][0:2])+'/'+bdt[0][2:4]+'/'+bdt[1]
				print "--"+bd

		if len(bdt) == 1:
			bd = str(bdt[0][0:2])+'/'+str(bdt[0][2:4])+'/'+bdt[0][4:10]

		if len(bd) == 10:
			cur.execute('replace into log (id,birthday) values("'+str(resu[0])+'","'+bd+'")')
			print resu[0],bd
	
	if resu[7] and len(resu[7]) < 10 :
		print resu[7]	


connection.commit() 
