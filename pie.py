#!/usr/bin/env python
# vim:ts=4:sw=4:et
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Copyright 2010 Fernando Henrique R. Silva (liquuid@gmail.com)
# http://www.linuxmafia.com.br

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
