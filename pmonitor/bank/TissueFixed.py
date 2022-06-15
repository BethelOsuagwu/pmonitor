# -*- coding: utf-8 -*-
from .Tissue import Tissue;

class TissueFixed(Tissue):
  
   
    
    def __init__(self,code,pressureTimeThreshold,effectEstimator,k_dpi=1,k_iri=0,k_gi=0,reliefTimeThreshold=5):
        """
        TissueFixed uses an integrator to accumulate damage. For relief, its  
        approach is to set a fixed period after which the total accumulated  
        effect decays to zero as in \cite{temes1977pressure,linder2009real}.
    
        
        reliefTimeThreshold : float
            The relief time threshold in seconds which determines how long a 
            relief period is required before pressure relieve can accur.
        
        References: 
            \cite{temes1977pressure} Temes, W.C. and Harder, P., 1977. Pressure relief training device. Physical therapy, 57(10), pp.1152-1153. doi:10.1093/ptj/57.10.1152
            
            \cite{linder2009real} Linder-Ganz, E., Yarnitzky, G., Yizhar, Z., Siev-Ner, I. and Gefen, A., 2009. Real-time finite element monitoring of sub-dermal tissue stresses in individuals with spinal cord injury: toward prevention of pressure ulcers. Annals of biomedical engineering, 37(2), pp.387-400.
        """
        
        
        self.reliefTimeThreshold=reliefTimeThreshold;
        
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
        if((self.reliefCounter*dt)>=self.reliefTimeThreshold): # Relief the effect
            self.iri=0;
        else:# Normal accumulation of effect
            self.iri=self.iri+self.k_iri * q; # integrator
        
        
        # Introduce non-linearity to remove negative values
        self.iri=max(self.iri,0) # ReLU 
        
        

    def _stepDpi(self,dt):
        
         # Compute the current effect
        q=self.q(P=self.P,dt=dt);
        
        #
        if((self.reliefCounter*dt)>=self.reliefTimeThreshold): # Relief the effect
            self.dpi=0;
        else:# Normal accumulation of effect
            self.dpi=self.dpi+ self.k_dpi * q; # integrator
        
        
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
        if((self.reliefCounterGi*dt)>=self.reliefTimeThreshold): # Relief the effect
            self.gi=0;
        else:# Normal accumulation of effect
            self.gi=self.gi+ self.k_gi *q; # integrator
        
        
        # Introduce non-linearity to remove negative values
        self.gi=max(self.gi,0); # ReLU 
        
    