# -*- coding: utf-8 -*-
import numpy as np;
import matplotlib.pyplot as plt;
from pmonitor.bank.TissueInverse import TissueInverse;
from pmonitor.bank.TissueFixed import TissueFixed;
from pmonitor.bank.TissueContinuous import TissueContinuous;
from pmonitor.bank.TissueLinear import TissueLinear;
from pmonitor.bank.TissueAveraging import TissueAveraging;

from pmonitor.inc.PressureTimeThreshold import PressureTimeThreshold;
from pmonitor.inc.EffectEstimator import EffectEstimator;
from pmonitor.inc.Helpers import Helpers;



# EXPERIMENTATION - Test responses given an impulse input
# Initialise
dt=0.1; # Sampling time
linear_beta=Helpers.linearBeta(28*24*60*60,dt); # Determine linear beta for 28 days
beta=Helpers.beta(5*60,dt); # Determine beta for 5 minutes
ptt=PressureTimeThreshold(); # Define pressure time injury threshold
ee=EffectEstimator(); # Define effect estimator

flen=round(5*60/dt); # Determine the averaging filter length for 5 minutes



# Create tissues
tissues=[];
tissueFixed=TissueFixed('default',ptt,ee);
tissueInverse=TissueInverse('default',ptt,ee);
tissueContinuous=TissueContinuous('default',ptt,ee,beta,beta,beta);
tissueLinear=TissueLinear('default',ptt,ee,linear_beta,linear_beta,linear_beta);
tissueAvg=TissueAveraging('default-a',ptt,ee,flen,flen,flen);

# Simulation params
nsteps=5000;# Number of simulation time/steps


# Impulse input
Ps=np.zeros(nsteps);
Ps[round(nsteps/4)]=10;

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



# Plot results together
## Apply some scalling
data_tissue_fixed_h=np.array(data_tissue_fixed_h)*1000000;
data_tissue_inverse_h=np.array(data_tissue_inverse_h)*1000000;
data_tissue_continuous_h=np.array(data_tissue_continuous_h)*1000000;
data_tissue_linear_h=np.array(data_tissue_linear_h)*1000000;
data_tissue_avg_h=np.array(data_tissue_avg_h)*1000000000;

plt.rcParams.update({'font.size': 13})


fig,ax1=plt.subplots();
t=np.array([x for x in range(nsteps)],np.float)*dt
lines1=ax1.plot(t,data_tissue_fixed_h,'--')
lines2=ax1.plot(t,data_tissue_inverse_h,'-.')
lines3=ax1.plot(t,data_tissue_continuous_h,':')
lines4=ax1.plot(t,data_tissue_avg_h,'-')
lines5=ax1.plot(t,data_tissue_linear_h,':')

ax1.set_ylabel('Effect * s (x $10^{-6}$)')
ax1.set_xlabel('Time (s)')


color = '#000000';
color_fainted='#666666';
color_alpha=0.1;
ax2=ax1.twinx();
lines0=ax2.plot(t,Ps,'-',color=color,alpha=color_alpha)
ax2.set_ylabel('Pressure (kPa)',color=color_fainted)
ax2.tick_params(axis='y', labelcolor=color_fainted)


plt.legend(lines0+lines1+lines2+lines3+lines4+lines5,['Pressure','TissueFixed','TissueInverse','TissueContinuous','Averaging $x10^{-3}$','Linear'],loc=0);


plt.title('Impulse response')
plt.savefig('img/impulse_response_compare.pdf');


