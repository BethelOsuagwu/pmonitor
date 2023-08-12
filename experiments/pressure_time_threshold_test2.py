# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 12:35:24 2021

@author: Bethel
Pressure-time cell death threshold testing
"""
import numpy as np;
import matplotlib.pyplot as plt;
from pmonitor.inc.PressureTimeThreshold import PressureTimeThreshold


ptt=PressureTimeThreshold();

data=np.array([[0,0]],np.float);
data=np.delete(data,0,axis=0);
for i in range(9,32):
    tp=ptt.pressureToTime(i);
    t=tp[0];
    P=tp[1];
    data=np.append(data,[[P,t]],axis=0)


plt.plot(data[:,1],data[:,0])
plt.xlabel('Time(minutes)')
plt.ylabel('Pressure (kPa)')
plt.title('Pressure-time cell death threshold');
plt.savefig('img/pressure_time_cell_death.pdf')