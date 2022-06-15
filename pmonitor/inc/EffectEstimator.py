# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 21:28:38 2021

@author: Bethel Osuagwu
"""
class EffectEstimator:
    # Linear model parameters. Parameters derived with Daniel et al. 1985 pigs data in 
    # MATLAB (/data/daniel1985pressure/regression_test.m)
    t_TERM=0.14938;
    P_TERM=0.0014787;
    CONSTANT_TERM=0;
    
    # Estimator type
    ESTIMATOR='linear';
    
    def __init__(self,estimator=None,t_term=None,P_term=None,constant_term=None):
        """
        The effect estimator class.

        Parameters
        ----------
        estimator : string|callable, optional
            String: Type of estimator, 'linear', 'pti' (pressure time integral).
            Function: A collable(P,t) that accepts the pressure(kPa) and time(minutes) 
            The default is string, 'linear'.
        t_term : float, optional
            The t term in the default linear model for effect estimator. The 
            term must be estimated with the time in minutes. 
            The default is None.
        P_term : float, optional
            The P term in the default linear model for effect estimator. The 
            term must be estimated with the P in kPa. 
            The default is None.
        constant_term : float, optional
            The constant term in the default linear model for effect estimator. The default is None.

        Returns
        -------
        None.

        """
        self.k_t=t_term or self.t_TERM;
        self.k_P=P_term or self.P_TERM;
        self.k_constant = constant_term or self.CONSTANT_TERM;
        self.estimator=estimator or self.ESTIMATOR;
        
        
    def q(self,P,t,samplingInterval=None):
        
        
        """
        The effect estimator, i.e. determine pressure-time total damage.

        Parameters
        ----------
        P : float
            Pressure in kPa.
        t : float
            The time of application of pressure in minutes.
        samplingInterval : float
            The time step in minutes for summing the value of the effect i.e 
            which makes the returned value independent of sampling interval. 
            Note that this means that we are summing/integrating the effect 
            over time and are effectively taking measurement at every minute 
            as a default rate of measurement of effect.
            The default is input param t.

        Returns
        -------
        float
            Estimated damage magnitude. The unit of the value depends on the 
            estimator. For estimator='pti' the unit is kPa.minutes.   

        """
        estimator=self.estimator;
        
        # Set the default for t.
        samplingInterval=samplingInterval or t;
        
        #
        q_e=None;# q estimate.
        
        if(callable(estimator)):
          q_e=estimator(P,t);
        elif(P==0):
            # We manually force the output to be zero since it does 
            # not make a physical sense for there to be an output 
            # greater than zero when P=0.
            q_e=0;
        elif(estimator=='linear'):
            
            k_c=self.k_constant
            k_t=self.k_t;
            k_P=self.k_P;
            
            
            q_e= k_c + k_t*t + k_P*P;
        
        
        elif(estimator=='pti'):
            q_e=t*P;
            
        return q_e*samplingInterval;
    