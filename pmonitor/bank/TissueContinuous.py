# -*- coding: utf-8 -*-
import numpy as np;
from .Tissue import Tissue;

class TissueContinuous(Tissue):
  
   
    
    def __init__(self,code,pressureTimeThreshold,effectEstimator,beta_dpi=1,beta_iri=1,beta_gi=1,k_dpi=1,k_iri=0,k_gi=0):
        """
        TissueContinuous implements comtiuous relief of accumulated effect 
        based on the ratio of the current applied load to the max applicable 
        load.

        """
        
        Tissue.__init__(self,code,pressureTimeThreshold,effectEstimator,beta_dpi,beta_iri,beta_gi,k_dpi,k_iri,k_gi);
        
        
        self._damage_method='continouse-load-ratio';
        
        # Set the minimum damaging pressure value
        self.Pmin=self.pressureTimeThreshold.getLongTermThreshold();
        

    def _stepIri(self,dt):
        
        
        # Compute the qmin(minumum damaging q) as the Pmin applied for dt duration.
        qmin=self.q(self.Pmin,dt);
        
        # Compute q for determining relief
        P_avg=np.mean(self.Ps);
        q_relief=self.q(P=P_avg,dt=dt);
        
         # Compute u
        u=min(q_relief,qmin)/qmin;
        
        # Compute the current effect
        q=self.q(P=self.P,dt=dt);
        
        
       
        
        # Filter
        self.iri=self.k_iri*q+(1-self.beta_iri*(1-u))*self.iri;
        
        
        # Introduce non-linearity to remove negative values
        self.iri=max(self.iri,0) # ReLU 
        
        

    def _stepDpi(self,dt):
        
        # Compute the qmin(minumum damaging q) as the Pmin applied for dt duration.
        qmin=self.q(self.Pmin,dt);
        
        # Compute q for determining relief
        P_avg=np.mean(self.Ps);
        q_relief=self.q(P=P_avg,dt=dt);
        
        # Compute u
        u=min(q_relief,qmin)/qmin;
        
        # Compute the current effect
        q=self.q(P=self.P,dt=dt);
        
        
        
        
        # Filter
        self.dpi=self.k_dpi*q+(1-self.beta_dpi*(1-u))*self.dpi;
        
        
        # Introduce non-linearity to remove negative values
        self.dpi=max(self.dpi,0) # ReLU 
        
    
    def _stepGi(self,dt,Tissues=[]):
        
        # Pressure gradient
        G=0;
        G_avg=0;
        for T in Tissues:
            G=G+abs(self.P - T.P);
            G_avg=G_avg+abs(np.mean(self.Ps) - np.mean(T.Ps));
        G=G/2.0;
        G_avg=G_avg/2.0;
        
        
        # Compute the qmin(minumum damaging q) as the Pmin applied for dt duration.
        qmin=self.q(self.Pmin,dt);
        
        # Compute q for determining relief
        q_relief=self.q(P=G_avg,dt=dt);
        
        # Compute u
        u=min(q_relief,qmin)/qmin;
        
        # Compute the current effect
        q=self.q(P=G,dt=dt);
        
        
        
        
        # Filter
        self.gi=self.k_gi*q+(1-self.beta_gi*(1-u))*self.gi;
        
        # Introduce non-linearity to remove negative values
        self.gi=max(self.gi,0); # ReLU 
        
    