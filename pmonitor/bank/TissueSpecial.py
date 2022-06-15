# -*- coding: utf-8 -*-
from .Tissue import Tissue;

class TissueSpecial(Tissue):
  
   
    
    def __init__(self,code,pressureTimeThreshold,effectEstimator,beta_dpi=1,beta_iri=1,beta_gi=1,k_dpi=1,k_iri=0,k_gi=0):
        """
        TissueSpecial implements the special case filter where the input pressure 
        signal is assumed to be stationary. Effect will be incorectly 
        estimated if the input is not stationary.

        """
        
        Tissue.__init__(self,code,pressureTimeThreshold,effectEstimator,beta_dpi,beta_iri,beta_gi,k_dpi,k_iri,k_gi);
        
        
        
        self._damage_method='normal-stationary-pressure';
        

    def _stepIri(self,dt):
        
        # Filter
        q=self.q(P=self.P,dt=dt);
        self.iri=self.iri*(1-self.beta_iri)+self.k_iri*q*(1+(self.n)*self.beta_iri);
        
        
        # Introduce non-linearity to remove negative values
        self.iri=max(self.iri,0) # ReLU 
        
        

    def _stepDpi(self,dt):
        
        # Filter
        q=self.q(P=self.P,dt=dt);
        self.dpi=self.dpi*(1-self.beta_dpi)+self.k_dpi*q*(1+self.n*self.beta_dpi);
        
       
        
        # Introduce non-linearity to remove negative values
        self.dpi=max(self.dpi,0) # ReLU 
        
    
    def _stepGi(self,dt,Tissues=[]):
        
        # Pressure gradient
        G=0;
        for T in Tissues:
            G=G+abs(self.P - T.P);
        G=G/2.0;
        
        
        
        # Filter
        q=self.q(P=G,dt=dt);
        self.gi=self.gi*(1-self.beta_gi)+self.k_gi*q*(1+self.n*self.beta_gi);
        
        
        
        # Introduce non-linearity to remove negative values
        self.gi=max(self.gi,0); # ReLU 
        
    