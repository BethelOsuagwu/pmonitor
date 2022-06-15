# -*- coding: utf-8 -*-
import numpy as np;
import matplotlib.pyplot as plt;
from pmonitor.bank.TissueContinuous import TissueContinuous;
from pmonitor.bank.TissueAveraging import TissueAveraging;
from pmonitor.inc.PressureTimeThreshold import PressureTimeThreshold;
from pmonitor.inc.EffectEstimator import EffectEstimator;
from pmonitor.inc.Helpers import Helpers;



# EXPERIMENTATION - Test responses given an finite step input
# Initialise
dt=0.1; # Sampling time
beta=Helpers.beta(5*60,dt); # Determine beta for 5 minutes
ptt=PressureTimeThreshold(); # Define pressure time injury threshold
ee=EffectEstimator(); # Define effect estimator

flen=round(5*60/dt); # Determine the averaging filter length for 5 minutes

# Create tissues
tissueContinuous=TissueContinuous('default-s',ptt,ee,beta,beta,beta);
tissueAvg=TissueAveraging('default-a',ptt,ee,flen,flen,flen);


# Simulation params
nsteps=5000;# Number of simulation time/steps


# Finite step input
Ps=np.zeros(nsteps);
Ps[round(nsteps/10):round(nsteps/4*3.8)]=20;

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
# Apply some calling
data_tissue_avg_h=np.array(data_tissue_avg_h)*1000;

plt.rcParams.update({'font.size': 13})


fig,ax1=plt.subplots();
t=np.array([x for x in range(nsteps)],np.float)*dt
lines3=ax1.plot(t,data_tissue_continuous_h,':')
lines4=ax1.plot(t,data_tissue_avg_h,'-')


ax1.set_ylabel('Effect')
ax1.set_xlabel('Time (s)')


color = '#000000';
color_fainted='#666666';
color_alpha=0.1;
ax2=ax1.twinx();
lines0=ax2.plot(t,Ps,'-',color=color,alpha=color_alpha)
ax2.set_ylabel('Pressure (kPa)',color=color_fainted)
ax2.tick_params(axis='y', labelcolor=color_fainted)


plt.legend(lines0+lines3+lines4,['Pressure','TissueContinuous','Averaging $x10^{-3}$'],loc=2);

plt.title('Finite step response')
plt.savefig('img/finite_step_response_with_continuous.pdf')