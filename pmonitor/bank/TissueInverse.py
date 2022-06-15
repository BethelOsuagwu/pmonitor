# -*- coding: utf-8 -*-
from .Tissue import Tissue;

class TissueInverse(Tissue):
  
   
    
    def __init__(self,code,pressureTimeThreshold,effectEstimator,k_dpi=1,k_iri=0,k_gi=0):
        """
        
        TissueInverse uses an integrator to accumulate damage.

        TissueInverse implements also the  method of applying relief as described
        in \cite{luboz2018personalized}. With this method, the inverse of the 
        time length of pressure-relief is multiplied by the accumulated effect
        for proportional effect relief.
        
        References: 
            \cite{luboz2018personalized} Luboz, V., Bailet, M., Grivot, C.B., Rochette, M., Diot, B., Bucki, M. and Payan, Y., 2018. Personalized modeling for real-time pressure ulcer prevention in sitting posture. Journal of tissue viability, 27(1), pp.54-58.
        """
        
        Tissue.__init__(self,code,pressureTimeThreshold,effectEstimator,0,0,0,k_dpi,k_iri,k_gi);
        
        
        self._damage_method='integrator';
        self._relief_method='inverse-relief-time';# \cite{luboz2018personalized}
        
        # Set the minimum damaging pressure value
        self.Pmin=self.pressureTimeThreshold.getLongTermThreshold();
        
        # Used to capture the value of accumulated effect before the start of a laod relief.
        self.iri_before_relief=0;
        self.dpi_before_relief=0;
        self.gi_before_relief=0;
        
        # A counter for the length of time(in samples) for a relief for GI.
        self.reliefCounterGi=0;
        
    

    def _stepIri(self,dt):
        
        
        # Compute the current effect
        q=self.q(P=self.P,dt=dt);
        
            
        #
        if(self.reliefCounter>0): # Relief the effect
            relief_secs=self.reliefCounter*dt;
            if relief_secs<1:
                relief_secs=1;
            self.iri=self.iri_before_relief * 1/(relief_secs);
        else:# Normal accumulation of effect
            self.iri=self.iri+self.k_iri * q; # integrator
            self.iri_before_relief=self.iri; # Keeping a copy of the effect incase a relef occurs next.
        
        
        
        # Introduce non-linearity to remove negative values
        self.iri=max(self.iri,0) # ReLU 
        
        

    def _stepDpi(self,dt):
        
         # Compute the current effect
        q=self.q(P=self.P,dt=dt);
        

        #
        if(self.reliefCounter>0): # Relief the effect
            relief_secs=self.reliefCounter*dt;
            if relief_secs<1:
                relief_secs=1;
            self.dpi=self.dpi_before_relief * 1/relief_secs;
        else:# Normal accumulation of effect
            self.dpi=self.dpi+ self.k_dpi * q; # integrator
            self.dpi_before_relief=self.dpi; # Keeping a copy of the effect incase a relef occurs next.
        
        
        
        
        # Introduce non-linearity to remove negative values
        self.dpi=max(self.dpi,0) # ReLU 
        
    
    def _stepGi(self,dt,Tissues=[]):
        
        # Pressure gradient
        G=0;
        for T in Tissues:
            G=G+abs(self.P - T.P);
        G=G/2.0;
        
        
        # Compute the current effect
        q=self.q(P=G,dt=dt);
        
        
        # Update the specific Gi counter
        self.reliefCounterGi=self.countRelief(G,self.reliefCounterGi);
        
        #
        if(self.reliefCounterGi>0): # Relief the effect
            relief_secs=self.reliefCounterGi*dt;
            if relief_secs<1:
                relief_secs=1;
            self.gi=self.gi_before_relief * 1/relief_secs;
        else:# Normal accumulation of effect
            self.gi=self.gi+ self.k_gi *q; # integrator
            self.gi_before_relief=self.gi; # Keeping a copy of the effect incase a relef occurs next.
        
        
        
        # Introduce non-linearity to remove negative values
        self.gi=max(self.gi,0); # ReLU 
        
    