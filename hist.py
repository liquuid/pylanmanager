#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import sys
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

mu, sigma = 20, 15
#x = mu + sigma*np.random.randn(10)

try: 
	sys.argv[1]
except:
	sys.exit()
x = sys.argv[1].split(',')
y = []
#x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,2,12,12,13,14,15,16,12,13,20,23,25,20,30,50,12]
for i in x:
	y.append(int(i))

x = y
print type(x[0])
   
# the histogram of the data
#n, bins, patches = plt.hist(x,100, normed=1, facecolor='green', alpha=0.75)
plt.hist(x)

#print n # bins , patches

# add a 'best fit' line
#y = mlab.normpdf( bins, mu, sigma)
#l = plt.plot(bins, y, 'r--', linewidth=1)
    
plt.xlabel('Idade')
plt.ylabel('Público')
plt.title('Histograma por idade:')
#plt.axis([0, 100, 0, 4])
plt.grid(True)
 
plt.show()
    

