# A pressure monitoring approach for pressure ulcer prevention
This is a Python experimentation of a prolonged tunable pressure monitoring approach for pressure ulcer prevention.

# Publications
Osuagwu, B., McCaughey, E. & Purcell, M. *A pressure monitoring approach for pressure ulcer prevention*. BMC Biomedical Engineering 5, 8 (2023). [https://doi.org/10.1186/s42490-023-00074-6](https://doi.org/10.1186/s42490-023-00074-6)

## Installation
Clone this repository.

## How to use
To monitor a tissue for a pressure ulcer prevention experiment, you will need to select a tissue implementation. The implemenations differs based on how they accumulate and relief the impact of an applied load. The various implentation are in /pmonitor/bank.

To perform the experiment:
1. Initialise a tissue implementation
```py
from pmonitor.bank.TissueLinear import TissueLinear;
from pmonitor.inc.PressureTimeThreshold import PressureTimeThreshold;
from pmonitor.inc.EffectEstimator import EffectEstimator;
from pmonitor.inc.Helpers import Helpers;


dt=0.1; # Sampling time.
linear_relief_time=5*60;# The recovery time. For 5 minutes.
linear_beta=Helpers.linearBeta(linear_relief_time,dt); # Determine linear beta. 
data_tissue_linear_h=[];# Will hold the tissue health statuses

ptt=PressureTimeThreshold(); # Define pressure time injury threshold.
ee=EffectEstimator(); # Define effect estimator.

# Initialise
tissueLinear=TissueLinear('default-l',ptt,ee,linear_beta,linear_beta,linear_beta);

```
2. Apply a load
```py
P=20; # Pressure of 20kPa.
tissueLinear.setP(P);
```
3. Take a unit time step of the tissue and inspect its health
```py
tissueLinear.step(dt);# Take a unit time step.
data_tissue_linear_h.append(tissueLinear.health(dt)); # Record the current health.
```
4. Indicate for pressure relief if the latest entry in data_tissue_linear_h is too high. 
5. Repeat from #3, or from #2 if the load changes. 

## Examples
The files 'script_*' provides demonstration of how to run an experiment.


