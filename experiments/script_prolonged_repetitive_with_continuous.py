# -*- coding: utf-8 -*-

import numpy as np;
import matplotlib.pyplot as plt;
from pmonitor.bank.TissueContinuous import TissueContinuous;
from pmonitor.bank.TissueAveraging import TissueAveraging;
from pmonitor.inc.PressureTimeThreshold import PressureTimeThreshold;
from pmonitor.inc.EffectEstimator import EffectEstimator;
from pmonitor.inc.Helpers import Helpers;
from scipy import signal


# EXPERIMENTATION - Test responses given a stationary input
# Initialise
dt=0.1; # Sampling time
relief_time=3*60*60; # Reliefe time in seconds
beta=Helpers.beta(relief_time,dt); # Determine beta.
ptt=PressureTimeThreshold(); # Define pressure time injury threshold
ee=EffectEstimator(); # Define effect estimator

flen=round(5*60/dt); # Determine the averaging filter length for 5 minutes


# Create tissues
tissueContinuous=TissueContinuous('default-c',ptt,ee,beta,beta,beta);
tissueAvg=TissueAveraging('default-a',ptt,ee,flen,flen,flen);

# Simulation params
nsteps=144000# Number of simulation time/steps


# Repetitive input
Ps=np.zeros(nsteps);
ifreq=1/(30*60);# The freqnency of the input signal in Hz.
dtn=[n*dt for n in range(0,nsteps)];
dtn=np.array(dtn,np.float);

Ps = 20*signal.square(2 * np.pi * ifreq * dtn);
Ps[Ps<0]=0;

# Add pressure relief after 2 hours
Ps[dtn>=2*60*60]=0;

# Define vars for collecting state data
data_tissue_continuous_h=[];
data_tissue_avg_h=[];

# Run simulation
for n in range(0,nsteps):
    
    # Set tissue interface pressure
    tissueContinuous.setP(Ps[n])
    tissueAvg.setP(Ps[n])
    
    # Step the tissues one time step to compute effects
    tissueContinuous.step(dt);
    tissueAvg.step(dt);
    
    # Record state data
    data_tissue_continuous_h.append(tissueContinuous.health(dt))
    data_tissue_avg_h.append(tissueAvg.health(dt));

# Plot results
# Apply some scalling
data_tissue_avg_h=np.array(data_tissue_avg_h)*10000;
plt.rcParams.update({'font.size': 13})


fig,ax1=plt.subplots();
t=np.array([x for x in range(nsteps)],np.float)*dt/(60*60)
lines3=ax1.plot(t,data_tissue_continuous_h,':')
lines4=ax1.plot(t,data_tissue_avg_h,'-')


ax1.set_ylabel('Effect')
ax1.set_xlabel('Time (h)')


color = '#000000';
color_fainted='#666666';
color_alpha=0.1;
ax2=ax1.twinx();
lines0=ax2.plot(t,Ps,'-',color=color,alpha=color_alpha)
ax2.set_ylabel('Pressure (kPa)',color=color_fainted)
ax2.tick_params(axis='y', labelcolor=color_fainted)


plt.legend(lines0+lines3+lines4,['Pressure','TissueContinuous','Averaging $x10^{-4}$'],loc=0);
plt.title('Repetitive input response (mean pressure:'+str(round(np.mean(Ps)))+'kPa),')
plt.savefig('img/prolonged/prolonged_repetitive_with_continuous.pdf')


