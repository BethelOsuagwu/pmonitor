# -*- coding: utf-8 -*-
import math;
import numpy as np;
import matplotlib.pyplot as plt;
from pmonitor.bank.TissueContinuous import TissueContinuous;
from pmonitor.bank.TissueAveraging import TissueAveraging;
from pmonitor.inc.PressureTimeThreshold import PressureTimeThreshold;
from pmonitor.inc.EffectEstimator import EffectEstimator;
from pmonitor.inc.Helpers import Helpers;



# EXPERIMENTATION - Test responses given a sinusoidal input
# Initialise
dt=0.1; # Sampling time
beta=Helpers.beta(5*60,dt); # Determine beta for 5 minutes
ptt=PressureTimeThreshold(); # Define pressure time injury threshold
ee=EffectEstimator(); # Define effect estimator

flen=round(5*60/dt); # Determine the averaging filter length for 5 minutes


# Create tissues
tissues=[];
tissueContinuous=TissueContinuous('default-s',ptt,ee,beta,beta,beta);
tissueAvg=TissueAveraging('default-a',ptt,ee,flen,flen,flen);

# Simulation params
nsteps=5000;# Number of simulation time/steps


# Sinusoidal input
Ps=np.zeros(nsteps);
ifreq=0.00333;# The freqnency of the input signal in Hz.
for n in range(0,nsteps):
    Ps[n]=20* math.sin(2*math.pi*ifreq*n*dt);

Ps[Ps<0]=0;# Remove zeros

# Define vers for collecting state data
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
    data_tissue_continuous_h.append(tissueContinuous.health(dt));
    data_tissue_avg_h.append(tissueAvg.health(dt));


# Plot results
# Apply some scalling
data_tissue_avg_h=np.array(data_tissue_avg_h)*1000;
plt.rcParams.update({'font.size': 13})

fig,ax1=plt.subplots();
t=np.array([x for x in range(nsteps)],np.float)*dt
lines2=ax1.plot(t,data_tissue_continuous_h,'-.')
lines4=ax1.plot(t,data_tissue_avg_h,'-')

ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Effect')

color = '#000000';
color_fainted='#666666';
color_alpha=0.1;
ax2=ax1.twinx();
lines0=ax2.plot(t,Ps,'-',color=color,alpha=color_alpha)
ax2.set_ylabel('Pressure (kPa)',color=color_fainted)
ax2.tick_params(axis='y', labelcolor=color_fainted)


plt.legend(lines0+lines2+lines4,['Pressure','TissueContinuous','Averaging $x10^{-3}$'],loc=9);
plt.title('Sinusoidal response')
plt.savefig('img/sinusoidal_input_response_with_continuous.pdf')
