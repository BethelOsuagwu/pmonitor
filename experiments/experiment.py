# -*- coding: utf-8 -*-
import numpy as np;
from random import random;
import matplotlib.pyplot as plt;
from pmonitor.bank.Tissue import Tissue;
from pmonitor.inc.PressureTimeThreshold import PressureTimeThreshold;
from pmonitor.inc.EffectEstimator import EffectEstimator;
from pmonitor.inc.Helpers import Helpers;



# EXPERIMENTATION
# Initialise
dt=0.1;#Sampling time
beta=Helpers.beta(5*60,dt);

tissues=[];
for tn in range(0,9):
    t_temp=Tissue(
        't'+str(tn),
        PressureTimeThreshold(),
        EffectEstimator(),
        beta,beta,beta);
    
    # attach a var for own use
    t_temp.h=[];
    t_temp.t=[];
    t_temp.ip=[];
    
    #
    tissues.append(t_temp);
    


# Run
nsteps=5000;#simulation time/steps
plt.axis();



Ps=np.zeros(nsteps);#interface pressure for tissue 5=>t4.

# Finite step input
#Ps[round(nsteps/4):round(nsteps/4*2)]=20;

# Impulse input
Ps[round(nsteps/4)]=1;

# Sinusoidal input
#for n in range(0,nsteps):
    #Ps[n]=20*math.sin(2*math.pi*0.00333*n*dt);
    #Ps[n]=20+100*random()

#

for n in range(0,nsteps):
    #print('Step: '+ str(n))
    
    
    # Set tissue interface pressure
    for T in tissues:
        if T.code=='t4':
            T.setP(Ps[n]);# Set a known pressure to the tissue of interest.
        else:
            T.setP(random()*0.00);
    
    
    # Step the tissues one time step
    for T in tissues:
        T.step(dt,tissues);
        
        # Record some data in our own vars
        T.h.append(T.health());
        T.t.append(n);
        T.ip.append(T.P);
     
    # Store health
    for T in tissues:
        h=T.health();





# Get health of the tissues
N=len(tissues);
legends=[];
for n in range(0,N):
    T=tissues[n];
    T.describe();
    plt.plot(T.t,T.h)
    legends.append(['Tissue '+str(T.code)]);


plt.xlabel('time/sample')
plt.ylabel('Health')
legends.append(['Pressure']);
plt.legend(legends);

