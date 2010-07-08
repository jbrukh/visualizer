'''
Created on Jul 8, 2010

@author: Administrator
'''

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.pyplot import *

fig = figure()
plt1 = fig.add_subplot(211)
plt2 = fig.add_subplot(212)

plt1.plot([1,2,3])
plt2.plot([3,4,5])

show()