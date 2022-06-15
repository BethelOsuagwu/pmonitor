# -*- coding: utf-8 -*-
import numpy as np;
import matplotlib.pyplot as plt;
from pmonitor.bank.Tissue import Tissue;
from pmonitor.bank.TissueBinned import TissueBinned;
from pmonitor.bank.TissueSpecial import TissueSpecial;
from pmonitor.bank.TissueAveraging import TissueAveraging;
from pmonitor.inc.PressureTimeThreshold import PressureTimeThreshold;
from pmonitor.inc.EffectEstimator import EffectEstimator;
from pmonitor.inc.Helpers import Helpers;



# EXPERIMENTATION - Test responses given an impulse input
# Initialise
dt=0.1; # Sampling time
beta=Helpers.beta(5*60,dt); # Determine beta for 5 minutes
ptt=PressureTimeThreshold(); # Define pressure time injury threshold
ee=EffectEstimator(); # Define effect estimator

flen=round(5*60/dt); # Determine the averaging filter length for 5 minutes

# Create tissues
tissues=[];
tissue=Tissue('default',ptt,ee,beta,beta,beta);
tissueBinned=TissueBinned('default',ptt,ee,beta,beta,beta);
tissueSpecial=TissueSpecial('default',ptt,ee,beta,beta,beta);
tissueAvg=TissueAveraging('default-a',ptt,ee,flen,flen,flen);

# Simulation params
nsteps=5000;# Number of simulation time/steps


# Impulse input
Ps=np.zeros(nsteps);
Ps[round(nsteps/4)]=10;

# Define vers for collecting state data
data_tissue_h=[];
data_tissue_binned_h=[];
data_tissue_special_h=[];
data_tissue_avg_h=[];

# Run simulation
for n in range(0,nsteps):
    
    # Set tissue interface pressure
    tissue.setP(Ps[n])
    tissueBinned.setP(Ps[n])
    tissueSpecial.setP(Ps[n])
    tissueAvg.setP(Ps[n])
    
    # Step the tissues one time step to compute effects
    tissue.step(dt);
    tissueBinned.step(dt);
    tissueSpecial.step(dt);
    tissueAvg.step(dt);
    
    # Record state data
    data_tissue_h.append(tissue.health(dt));
    data_tissue_binned_h.append(tissueBinned.health(dt));
    data_tissue_special_h.append(tissueSpecial.health(dt));
    data_tissue_avg_h.append(tissueAvg.health(dt));



# Plot results
# Apply some scalling
data_tissue_h=np.array(data_tissue_h)*1000;
data_tissue_binned_h=np.array(data_tissue_binned_h)*1000;
data_tissue_special_h=np.array(data_tissue_special_h)*1000;
data_tissue_avg_h=np.array(data_tissue_avg_h)*1000000;

plt.rcParams.update({'font.size': 13})


fig,ax1=plt.subplots();
t=np.array([x for x in range(nsteps)],np.float)*dt
lines1=ax1.plot(t,data_tissue_h,'--')
lines2=ax1.plot(t,data_tissue_binned_h,'-.')
lines3=ax1.plot(t,data_tissue_special_h,':')
lines4=ax1.plot(t,data_tissue_avg_h,'-')

ax1.set_ylabel('Effect (x $10^{-3}$)')
ax1.set_xlabel('Time (s)')


color = '#000000';
color_fainted='#666666';
color_alpha=0.1;
ax2=ax1.twinx();
lines0=ax2.plot(t,Ps,'-',color=color,alpha=color_alpha)
ax2.set_ylabel('Pressure (kPa)',color=color_fainted)
ax2.tick_params(axis='y', labelcolor=color_fainted)


plt.legend(lines0+lines1+lines2+lines3+lines4,['Pressure','Tissue','TissueBinned','TissueSpecial','Averaging $x10^{-3}$'],loc=0);


plt.title('Impulse response')
plt.savefig('img/impulse_response.pdf')