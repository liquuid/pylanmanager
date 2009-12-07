#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import sys
import matplotlib.pyplot as plt

mu, sigma = 20, 15

try: 
	sys.argv[1]
except:
	sys.exit()
x = sys.argv[1].split(',')
y = []
for i in x:
	y.append(int(i))

x = y
   
plt.hist(x)

plt.xlabel('Idade')
plt.ylabel('Publico')
plt.title('Histograma por idade:')
plt.grid(True)
 
plt.show()
