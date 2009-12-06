#!/usr/bin/env python
import sys
from pylab import *
    
    # make a square figure and axes
figure(1, figsize=(6,6))
ax = axes([0.1, 0.1, 0.8, 0.8])
    
labels = 'Mulheres, total= '+str(sys.argv[2]), 'Homens, total= '+str(sys.argv[3])
fracs = [20,80]

fracs = sys.argv[1].split(',')
#print temp

 
explode=(0, 0.05)
pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
title(sys.argv[4], bbox={'facecolor':'0.8', 'pad':5})
    
show()
