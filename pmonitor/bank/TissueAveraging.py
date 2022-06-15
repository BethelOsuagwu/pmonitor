import numpy as np;
from .Tissue import Tissue;


class TissueAveraging(Tissue):

    def __init__(self,code,pressureTimeThreshold,effectEstimator,len_dpi=1,len_iri=1,len_gi=1,k_dpi=1,k_iri=0,k_gi=0):
        """
        TissueAveraging uses the classic averaging filter approach to accumulate 
        ongoing effect.

        Parameters
        ----------
        
        len_dpi : integer, optional
            Averaging Filter length for DTI. The default is 1.
            TODO: CHANGE lend_dpi to len_dti
        len_iri : integer, optional
            Averaging  length for IRI. The default is 1.
        len_gi : integer, optional
            Averaging Filter length for GI. The default is 1.
        

        Returns
        -------
        None.

        """
        Tissue.__init__(self,code,pressureTimeThreshold,effectEstimator,0,0,0,k_dpi,k_iri,k_gi);
        
        
        self._damage_method='averaging';
        
        self._relief_method='averaging';
        
       
        # Buffers
        self.iri=np.array([0 for i in range(len_iri)],dtype=np.float_); #ischeamiaReperfutionInjury
        self.dpi=np.array([0]*len_dpi,dtype=np.float_); # deepTissueInjury
        self.gi=np.array([0]*len_gi,dtype=np.float_); # gradientInjury
   
       
        
    def _stepIri(self,dt):      
        
        #
        
        # Damage
        if(self.hasDamagingPressure()):
            d=self.k_iri*self.q(P=self.P,dt=dt);
        else:
            d=0;
            
        # First in first out. 
        L=len(self.iri);      
        self.iri[1:L-1]=self.iri[0:L-2];
        self.iri[0]=d;

        


    def  _stepDpi(self,dt):
        
        # Damage
        if(self.hasDamagingPressure()):
            d=self.k_dpi*self.q(P=self.P,dt=dt);
        else:
            d=0;
            
            
        # First in first out. 
        L=len(self.dpi);      
        self.dpi[1:L-1]=self.dpi[0:L-2];
        self.dpi[0]=d;
        # SAME AS:
        #self.dpi=np.concatenate(([d],self.dpi));
        #self.dpi=np.delete(self.dpi,L-1);
    
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
        
       # First in first out. 
        L=len(self.gi);      
        self.gi[1:L-1]=self.gi[0:L-2];
        self.gi[0]=d;
        
    
    def healthIri(self):
        """
        Compute Tissue Health for Ischaemia and reperfusion

        Returns
        -------
        Float
            Tissue health number for IRI.

        """
        return np.mean(self.iri);
    
    def healthDpi(self):
        """
        Compute Tissue Health for Deep Tissue Injury

        Returns
        -------
        Float
            Tissue health number for DPI.

        """
            
        return np.mean(self.dpi);
    
    def healthGi(self):
        """
        Compute Tissue Health for Gradient injury/damage

        Returns
        -------
        Float
            Tissue health number for GI.

        """
        return np.mean(self.gi);
