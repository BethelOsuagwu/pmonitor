import numpy as np;
from .Tissue import Tissue;


class TissueBinned(Tissue):
 
    def __init__(self,code,pressureTimeThreshold,effectEstimator,beta_dpi=1,beta_iri=1,beta_gi=1,k_dpi=1,k_iri=0,k_gi=0):
        """
        TissueBinned uses the bin method instead of filter to compute damage 
        effects. It does not respond to small pressure magnitudes determined 
        to be non-damaging.

        TODO: Let the supplied beta apply to the lowest bin. Higher bins will 
        get a lower beta to reflate their capacity to cause more damage. 
        """
        
        Tissue.__init__(self,code,pressureTimeThreshold,effectEstimator,beta_dpi,beta_iri,beta_gi,k_dpi,k_iri,k_gi);
        
        
        self._damage_method='binned';
        
       
        # Bins
        self.iri=np.array([0,0,0],dtype=np.float_); #ischeamiaReperfutionInjury
        self.dpi=np.array([0,0,0],dtype=np.float_); #deepTissueInjury
        self.gi=np.array([0,0,0],dtype=np.float_); # gradientInjury
   
        # Continously relief or relief only when there is none damaging pressure.
        self.continouse_relief=True;
        
    def _stepIri(self,dt):      
        
        #
        
        # Damage
        if(self.hasDamagingPressure()):
            d=self.k_iri*self.q(P=self.P,dt=dt);
        else:
            d=0;
        
        bin_idx=None;# Bin index
        if d < Tissue.DAMAGE_LOW:
            bin_idx=None;
        elif d < Tissue.DAMAGE_MID:
            bin_idx=0;
        elif d < Tissue.DAMAGE_HIGH:
            bin_idx=1;
        else:
            bin_idx=2; 
        
        # Overide the computed bin above and use a fixed bin if we 
        # are only performing pressure relieve when their is none 
        # damaging input pressure.
        if self.continouse_relief and (bin_idx is not None):
            bin_idx=0;
        
        
        if bin_idx is not None:
            self.iri[bin_idx]=self.iri[bin_idx] + d;
        
         # Relieve
        for bn in range(0,3):
            if(bin_idx is None or (bn != bin_idx)): # Ensures that we relieve only relieved effect
                r=self.beta_iri * self.iri[bn];
                self.iri[bn]=self.iri[bn] - r;
               
        
        # Introduce non-linearity to remove negative values
        self.iri[self.iri<0]=0; # ReLU 


    def  _stepDpi(self,dt):
        
        # Damage
        if(self.hasDamagingPressure()):
            d=self.k_dpi*self.q(P=self.P,dt=dt);
        else:
            d=0;
       
        
        bin_idx=None;# Bin index
        if d < Tissue.DAMAGE_LOW:
            bin_idx=None;
        elif d < Tissue.DAMAGE_MID:
            bin_idx=0;
        elif d < Tissue.DAMAGE_HIGH:
            bin_idx=1;
        else:
            bin_idx=2; 
        
        # Overide the computed bin above and use a fixed bin if we 
        # are only performing pressure relieve when their is none 
        # damaging input pressure.
        if self.continouse_relief and (bin_idx is not None):
            bin_idx=0;
        
        
       
        if bin_idx is not None:
            self.dpi[bin_idx]=self.dpi[bin_idx] + d;
        
        # Relieve
        for bn in range(0,3):
            if((bin_idx is None) or (bn != bin_idx)): # Ensures that we relieve only relieved effect
                r=self.beta_dpi * self.dpi[bn];#
                self.dpi[bn]=self.dpi[bn] - r;
        
        
        # Introduce non-linearity to remove negative values
        self.dpi[self.dpi<0]=0; # ReLU 
        
    
    def _stepGi(self,dt,Tissues=[]):
        
        # Damage
        G=0;#Pressure gradient
        for T in Tissues:
            G=G+abs(self.P - T.P);
            
        G=G/2.0;
            
        if(self.hasDamagingPressure()):
            d=self.k_gi*self.q(P=G,dt=dt);
        else:
            d=0;
        
        bin_idx=None;# Bin index
        if d < Tissue.DAMAGE_LOW:
            bin_idx=None;
        elif d < Tissue.DAMAGE_MID:
            bin_idx=0;
        elif d < Tissue.DAMAGE_HIGH:
            bin_idx=1;
        else:
            bin_idx=2; 
        
        # Overide the computed bin above and use a fixed bin if we 
        # are only performing pressure relieve when their is none 
        # damaging input pressure.
        if self.continouse_relief and (bin_idx is not None):
            bin_idx=0;
        
        
        if bin_idx is not None:
            self.gi[bin_idx]=self.gi[bin_idx] + d;
        
        # Relieve
        for bn in range(0,3):
            if(bin_idx is None or (bn != bin_idx)): # Ensures that we relieve only relieved effect
                r=self.beta_gi * self.gi[bn];#
                self.gi[bn]=self.gi[bn] - r;
           
        
        
        # Introduce non-linearity to remove negative values
        self.gi[self.gi<0]=0; # ReLU 
        
    
    def healthIri(self):
        """
        Compute Tissue Health for Ischaemia and reperfusion

        Returns
        -------
        Float
            Tissue health number for IRI.

        """
        return np.sum(self.iri);
    
    def healthDpi(self):
        """
        Compute Tissue Health for Deep Tissue Injury

        Returns
        -------
        Float
            Tissue health number for DPI.

        """
        return np.sum(self.dpi);
    
    def healthGi(self):
        """
        Compute Tissue Health for Gradient injury/damage

        Returns
        -------
        Float
            Tissue health number for GI.

        """
        return np.sum(self.gi);
