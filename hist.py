#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
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
