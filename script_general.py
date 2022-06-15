# -*- coding: utf-8 -*-

from pmonitor.bank.Tissue import Tissue;
from pmonitor.inc.PressureTimeThreshold import PressureTimeThreshold
from pmonitor.inc.EffectEstimator import EffectEstimator;


from pmonitor.inc.Helpers import Helpers;



# EXPERIMENTATION - Test responses given an finite step input
# Initialise
dt=0.1; # Sampling time
beta=Helpers.beta(5*60,dt); # Determine beta for 5 minutes
ptt=PressureTimeThreshold(); # Define pressure time injury threshold
ee=EffectEstimator(); # Define effect estimator

# Create tissue
tissue=Tissue('default',ptt,ee,beta,beta,beta);

# Plot tissue's impulse response
tissue.impulseResponse(dt);