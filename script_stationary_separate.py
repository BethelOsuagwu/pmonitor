# -*- coding: utf-8 -*-
from random import random;
import numpy as np;
import matplotlib.pyplot as plt;
from pmonitor.bank.TissueFixed import TissueFixed;
from pmonitor.bank.TissueInverse import TissueInverse;
from pmonitor.bank.TissueContinuous import TissueContinuous;
from pmonitor.bank.TissueLinear import TissueLinear;
from pmonitor.bank.TissueAveraging import TissueAveraging;
from pmonitor.inc.PressureTimeThreshold import PressureTimeThreshold;
from pmonitor.inc.EffectEstimator import EffectEstimator;
from pmonitor.inc.Helpers import Helpers;



# EXPERIMENTATION - Test responses given a stationary input
# Initialise
dt=0.1; # Sampling time
linear_relief_time=5*60;#for 5 minutes
linear_beta=Helpers.linearBeta(linear_relief_time,dt); # Determine linear beta 

relief_time=linear_relief_time;
beta=Helpers.beta(relief_time,dt); # Determine beta
ptt=PressureTimeThreshold(); # Define pressure time injury threshold
ee=EffectEstimator(); # Define effect estimator

flen=round(5*60/dt); # Determine the averaging filter length for 5 minutes


# Create tissues
tissues=[];
tissueFixed=TissueFixed('default',ptt,ee);
tissueInverse=TissueInverse('default',ptt,ee);
tissueContinuous=TissueContinuous('default',ptt,ee,beta,beta,beta);
tissueLinear=TissueLinear('default-l',ptt,ee,linear_beta,linear_beta,linear_beta);
tissueAvg=TissueAveraging('default-a',ptt,ee,flen,flen,flen);

# Simulation params
nsteps=5000;# Number of simulation time/steps


# Stationary input
Ps=np.zeros(nsteps);
for n in range(0,nsteps):
    Ps[n]=20+100*random(); # Or a varying stationary input

# Define vers for collecting state data
data_tissue_fixed_h=[];
data_tissue_inverse_h=[];
data_tissue_continuous_h=[];
data_tissue_linear_h=[];
data_tissue_avg_h=[];

# Run simulation
for n in range(0,nsteps):
    
    # Set tissue interface pressure
    tissueFixed.setP(Ps[n])
    tissueInverse.setP(Ps[n])
    tissueContinuous.setP(Ps[n])
    tissueLinear.setP(Ps[n])
    tissueAvg.setP(Ps[n])
    
    # Step the tissues one time step to compute effects
    tissueFixed.step(dt);
    tissueInverse.step(dt);
    tissueContinuous.step(dt);
    tissueLinear.step(dt);
    tissueAvg.step(dt);
    
    # Record state data
    data_tissue_fixed_h.append(tissueFixed.health(dt));
    data_tissue_inverse_h.append(tissueInverse.health(dt));
    data_tissue_continuous_h.append(tissueContinuous.health(dt));
    data_tissue_linear_h.append(tissueLinear.health(dt));
    data_tissue_avg_h.append(tissueAvg.health(dt));

# Plot results
# Apply some calling
data_tissue_fixed_h=np.array(data_tissue_fixed_h)*100;
data_tissue_inverse_h=np.array(data_tissue_inverse_h)*100;
data_tissue_continuous_h=np.array(data_tissue_continuous_h)*100;
data_tissue_linear_h=np.array(data_tissue_linear_h)*100;
data_tissue_avg_h=np.array(data_tissue_avg_h)*100000;
plt.rcParams.update({'font.size': 13})


t=np.array([x for x in range(nsteps)],np.float)*dt



#-----------------------------------------------------------
# Plot results on saparatly................................

title='Stationary input response (mean pressure:'+str(round(np.mean(Ps)))+'kPa)';
xlabel='Time (s)'
ylabel='Effect * s (x $10^{-2}$)';
annotations={'avg':'Average $x10^{-3}$ - L='+str(flen),
             'linear':'Linear - RT='+str(linear_relief_time) +'s',
             'continuous':'Exp - RT='+ str(relief_time) +'s'
             };
file_name='img/separate/stationary_input_response_compare_separate.pdf'

from pmonitor.inc.Analysis import plot_separate;
plot_separate(t,Ps,data_tissue_avg_h,data_tissue_fixed_h,data_tissue_inverse_h,data_tissue_continuous_h,data_tissue_linear_h,
              title,xlabel,ylabel,file_name,annotations)

