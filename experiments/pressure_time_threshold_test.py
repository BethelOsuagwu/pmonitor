# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 12:35:24 2021

@author: Bethel
Pressure-time cell death threshold testing
"""
import numpy as np;
import matplotlib.pyplot as plt;
from mpl_toolkits.mplot3d import Axes3D


K=23;
t0=90;
C=9;
a=0.15;
t=np.array(range(200))
P=(K/(1+np.exp(a*(t-t0))) ) +C;
Pt=P*t;


ax=plt.axes(projection='3d')
ax.plot(t,P,Pt)

ax.view_init(30, 20)

