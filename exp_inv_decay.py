# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 18:50:10 2021

@author: Bethel
"""
import numpy as np;
import matplotlib.pyplot as plt;

# Inverse vs Exponential function
t=[i for i in range(1,20)];
t=np.array(t);
y_inv=1/t;
y_exp=np.exp(-t);

plt.plot(t,y_inv);
plt.plot(t,y_exp);
plt.legend(['Inverse','Exponential']);