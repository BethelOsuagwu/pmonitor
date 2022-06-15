# -*- coding: utf-8 -*-
import numpy as np;
from ..inc.PressureTimeThreshold import PressureTimeThreshold;
from ..inc.EffectEstimator import EffectEstimator;
from ..inc.Helpers import Helpers;

class Tissue:

    # Instantaneous damage value that is considered harmless. 
    # THIS IS CURRENTLY BEIGN USED BY THE TissueBinned.
    DAMAGE_LOW=0.001;
    
    # Instantaneous damage value that is considered mid-level.
    # THIS IS CURRENTLY BEIGN USED BY THE TissueBinned.
    DAMAGE_MID=0.018;
    
    # Instantaneous damage value that is considered high.
    # THIS IS CURRENTLY BEIGN USED BY THE TissueBinned.
    DAMAGE_HIGH=0.04;
    
    # Value of accumulated damage for which cannot be relieved automatically 
    # because the tissue is believed to be damaged already
    ACCUMULATED_CRITICAl_DAMAGE=1000;#TODO : Implement this. Any value higher than this can not be auto relieved i.e irrelievable and sustained injury.
    
    """
    A damaging pressure require a short time, i.e the shorter the required 
    time the more damaging the pressure is expecially with respect to deep 
    pressure injury. So a pressure requiring a long period of time can be 
    considered none damaging.Here we define the corresponding times(in minutes) 
    for a damaging and non-damaging pressure magnitudes.
    HOWEVER NOT BEING USED BY DEFAULT @see self.hasDamagingPressure() WHICH 
    USES AN ALTERNATIVE METHOD TO DETERMINE HARMFUL AND NON-HARMFUL MAGNITUDES.
    """
    PRESSURE_TIME_THRESHOLD_SHORT_TIME=5;# i.e damaging pressure according to this definition.
    PRESSURE_TIME_THRESHOLD_LONG_TIME=180; # i.e non-damaging/harmless pressure according to this definition 
    
    def __init__(self,code,pressureTimeThreshold,effectEstimator,beta_dpi=1,beta_iri=1,beta_gi=1,k_dpi=1,k_iri=0,k_gi=0,history_len=50):
        """
        This base class Implements an approximation of the monitoring filter. It 
        saturates after a period of time. For the exact monitoring filter 
        use ..bank.TissueBinned

        Parameters
        ----------
        code : string
            Arbitrary idetifier.
        pressureTimeThNo docreshold : PressureTimeThreshold
            An instance of PressureTimeThreshold
        effectEtimator : Effect, optional
            The effect estimator
        beta_iri : float, optional
            Effect relieve rate for ischeamia & reperfusion injury. The default is 1.
        beta_dpi : float, optional
            Effect relieve rate for deep tissue injury. The default is 1.
            TODO:CHANGE beta_dpi to beta_dti  HERE AND IN CHILD CLASSES.
        beta_gi : float, optional
            Effect relieve rate for pressure gradient injury. The default is 1.
        k_dpi : float
            Damage contribution ratio for Deep tissue injury.
            A sum of this ratio with ratios of other damage contributors should
            sum to unity. The default is 1. 
            TODO:CHANGE k_dpi to k_dti  HERE AND IN CHILD CLASSES. 
        k_iri : float
            Damage contribution ratio for ischeamia & reperfusion injury. 
            A sum of this ratio with ratios of other damage contributors should
            sum to unity.The default is 0.
        k_gi : float
            Damage contribution ratio for pressure gradient injury.
            A sum of this ratio with ratios of other damage contributors should
            sum to unity. The default is 0.
        history_len : integer
            The length(in samples) of the tissue's history that should be kept. This for 
            exmaple determines the buffer length of pressure history that 
            should be kept for common filtering operations or reference 
            purpose. It is not directly or used related to computation of 
            effect.
            
        Returns
        -------
        None.

        """
        
        # States how the daage is accumulated
        self._damage_method='normal';
        
        # State how relief is applied
        self._relief_method='exponential-decay';
        
        # Tissue id
        self.code=code;
        
        # Relieve coefficient, beta defined as the rate of recovery from the 
        # accumulated effect of pressure below irrecoverable damage. 
        self.beta_iri=beta_iri; 
        self.beta_dpi=beta_dpi ;
        self.beta_gi=beta_gi;
        
        # Damage contributions
        self.k_iri=k_iri; # #ischeamiaReperfutionInjury
        self.k_dpi=k_dpi; # deepPressureInjury
        self.k_gi=k_gi; # gradientInjury
        
        
        
        
        self.iri=0; #ischeamiaReperfutionInjury
        self.dpi=0; # deepPressureInjury
        self.gi=0; # gradientInjury
        
        # Current Interface pressure
        self.P=0;
        
        # Stores the history of Ps up to a certain length
        self.Ps=[0]* history_len;
        
        # Pressure-time cell death threshold
        if(isinstance(pressureTimeThreshold, PressureTimeThreshold)):
            self.pressureTimeThreshold=pressureTimeThreshold;
        else:
            raise Exception('Parameter 2 must be an instance of PressureTimeThreshold');
            
        
        
        
        # Estimator
        if(isinstance(effectEstimator, EffectEstimator)):
            self.effectEstimator=effectEstimator;
        else:
            raise Exception('Parameter 3 must be an instance of EffectEstimator');
            
            
        # Sample counter
        self.n=-1;
        
        # A counter for the length of time(in samples) for a relief.
        self.reliefCounter=0;
        
        #
        self.reset();
        
    def reset(self):
        """
        Reset the Tissue to its initial state

        Returns
        -------
        None.

        """
        self.iri=0;
        self.dpi=0;
        self.gi=0; 

        self.P=0;
        self.Ps=[0]*len(self.Ps);
        
        
        self.n=-1;
    
    def impulseResponse(self,dt=1,typ='dpi'):
        """
        Impulse response of the monitoring filter.

        Parameters
        ----------
        dt : float
            Sampling time in seconds. The default is 1.
        typ : string
            The type of injury mechanism. The default is 'dpi'
        Returns
        -------
        None.

        """
        beta=self.beta_dpi;
        if(typ=='iri'):
            beta=self.beta_iri;
        elif(typ=='gi'):
            beta=self.beta_gi;
            
        Helpers.impulseResponse(beta,dt,True);
        
        
        
    def addToHistory(self):
        """
        Push current tissue state into history


        Returns
        -------
        None.

        """

        # First in first out
        L=len(self.Ps);
        self.Ps[1:L-1]=self.Ps[0:L-2];
        self.Ps[0]=self.P;
    
    def setP(self,P):
        """
        Set the current tissue interface pressure.
        
        Parameters
        ----------
        P : float
            Interface pressure (i.e.pressure on skin)

        Returns
        -------
        None.

        """
        self.P=P;
        self.addToHistory();
        
    def hasDamagingPressure(self,P=None):
        """
        Determines if the given or current pressure in the tissue is considered 
        damaging.
        
        Parameters
        ----------
        P : float
            Interface pressure (i.e.pressure on skin)

        Returns
        -------
        boolean
            Indicates if the current pressure is damaging or not.

        """
        use_smoothed_P_copy=False; #usign a smoothed P ensures we do not respond to transient changes
        
        if (P is not None):
            pass;
        elif use_smoothed_P_copy:
            L=round(10*5*10);
            if hasattr(self, 'Ps'):                  
                self.Ps[1:L-1]=self.Ps[0:L-2];
                self.Ps[0]=self.P;
            else:
                self.Ps=[self.P]*L;
            
            P=np.mean(self.Ps);
        else:
            P=self.P;
        
        use_pressure_value=True;
        
        if(use_pressure_value):
            return self.pressureTimeThreshold.isDamagingPressure(P);
        else:
            # If the t required to cause damage is too high, we think the pressure is not damaging.
            tp=self.pressureTimeThreshold.pressureToTime(P);
            return tp[0] < self.PRESSURE_TIME_THRESHOLD_LONG_TIME
    
    def q(self,P=None,dt=1):
        """
        Determine pressure-time total damage.

        Parameters
        ----------
        P : float, optional
            Pressure in kPa. The default is None.
        dt : float, optional
            Sampling time in seconds. The default is 1.
        

        Returns
        -------
        float
            Estimated damage magnitude.

        """
        
        
        P=P or self.P;
        t=dt/60; # We turn to minutes because model is in minutes
        
        return self.effectEstimator.q(P,t);
            
        
    def isRelief(self,P=None):
        """
        Check if based on the given or the current pressure, if we are having a 
        pressure relief.
        
        Parameters
        ----------
        P : float
            Interface pressure (i.e.pressure on skin)

        Returns
        -------
        Boolean.

        """
        
        if(self.hasDamagingPressure(P)):
            return False;
        else:
            return True;
        
    def countRelief(self,P=None,current_count=None):
        """
        Update the relief counter which keeps count of the length of the 
        relief period in smaples.
        
        Parameters
        ----------
        P : float
            Interface pressure (i.e.pressure on skin). The default is None.
        current_count : Integer
            The variable the holds the current count. If not provided the the 
            equivalent counter on the instance will be updated insted.

        Returns
        -------
        integer
            The updated count
        

        """
        original_count=current_count;
        if (original_count is None ):
            current_count=self.reliefCounter;
        
        is_relief=self.isRelief(P);
        
        # Count relief period in samples
        if(is_relief):                
            current_count=current_count+1;

        # Ensure the reliefcounter is zero when we are not relieving
        if(current_count and is_relief==False):
            current_count=0;
    
        
        #
        if (original_count is None ):
            self.reliefCounter=current_count;
            
        #
        return current_count;
    
    def step(self,dt,Tissues=[]):
        '''
        Compute the effect of the current applied pressure on the tissue for 
        one time step.

        Parameters
        ----------
        dt : float
            Sampling time step in seconds.
        Tissues : Arraylike, optional
            Neighbouring tissues. The default is [].

        Returns
        -------
        None.

        '''
        # ====================================================================
        #   Note: We start counting from the first time we have a non-zero 
        #   input pressure.
        # ====================================================================
        if(self.n>=0 or self.P>0):
            self.n+=1;
        
        # Update the relief counter
        self.countRelief();
        
        
        
        # step individual components
        self._stepIri(dt);
        self._stepDpi(dt);
        self._stepGi(dt,Tissues);
        
        
        
        
        
    
    # 
    def _stepIri(self,dt): 
        """
        Compute combined ischeamia and reperfusion tissue damage and 
        relieve

        Parameters
        ----------
        dt : float
            Sampling time step in seconds.

        Returns
        -------
        None.

        """
        
        
        # Filter
        q=self.q(P=self.P,dt=dt);
        self.iri=self.iri*(1-self.beta_iri)+self.k_iri*q*(1+self.beta_iri);
        
        
        # Introduce non-linearity to remove negative values
        self.iri=max(self.iri,0) # ReLU 
        
        

    def _stepDpi(self,dt):
        """
        Compute deep pressuretissue damage and relieve.
        TODO:CHANGE _stepDpi to _stepDti HERE AND IN CHILD CLASSES. 

        Parameters
        ----------
        dt : float
            Sampling time step in seconds.

        Returns
        -------
        None.

        """
        
        # Filter
        q=self.q(P=self.P,dt=dt);
        self.dpi=self.dpi*(1-self.beta_dpi)+self.k_dpi*q*(1+self.beta_dpi);
        
        
        # Introduce non-linearity to remove negative values
        self.dpi=max(self.dpi,0) # ReLU 
        
    
    
    def _stepGi(self,dt,Tissues=[]):
        """
        Compute gradient tissue damage and relieve

        Parameters
        ----------
        dt : float
            Sampling time step in seconds.
        Tissues : Tissue, optional
            List/Arraylike of Neighbouring tissues. The default is [].

        Returns
        -------
        None.

        """
        
        # Pressure gradient
        G=0;
        for T in Tissues:
            G=G+abs(self.P - T.P);
        G=G/2.0;
        
        
        
        # Filter
        q=self.q(P=G,dt=dt);
        self.gi=self.gi*(1-self.beta_gi)+self.k_gi*q*(1+self.beta_gi);
        
        
        
        # Introduce non-linearity to remove negative values
        self.gi=max(self.gi,0); # ReLU 
        
        
    def healthIri(self):
        """
        Compute Tissue Health for Ischaemia and reperfusion

        Returns
        -------
        Float
            Tissue health number for IRI.

        """
        return self.iri;
    
    def healthDpi(self):
        """
        Compute Tissue Health for Deep Tissue Injury.
        TODO: CHANGE _healthDpi to _healthDti HERE AND IN CHILD CLASSES.

        Returns
        -------
        Float
            Tissue health number for DPI.

        """
        return self.dpi;
    
    def healthGi(self):
        """
        Compute Tissue Health for Gradient injury/damage

        Returns
        -------
        Float
            Tissue health number for GI.

        """
        return self.gi;
    
    def health(self,dt=1):
        """
        Compute overall Tissue Health
        
        Parameters
        ----------
        dt : float
            Sampling time step in seconds.

        Returns
        -------
        Float
            Tissue health number.

        """
        # TODO: Multiplication by dt here is wrong since dt SHOULD HAVE already been used to compute the effect in the first place.
        return dt*(self.healthIri() + self.healthDpi() + self.healthGi());
    
    def info(self):
        """
        Print detils of the Tissue.

        Returns
        -------
        None.

        """
        print('_________________________')
        print ('Tissue code: '+self.code)
        print ('Tissue damage method: '+self._damage_method)
        print('------')
        
        print('COEFFICIENTS');
        print('ischeamiaReperfutionInjury: '+str(self.k_iri));
        print('deepTissueInjury: '+str(self.k_dpi)); 
        print('gradientInjury: '+str(self.k_gi));
        
        print('------')
        print('TIME CONSTANTS');
        print('ischeamiaReperfutionInjury: '+str(self.beta_iri)); 
        print('deepTissueInjury: '+str(self.beta_dpi));
        print('gradientInjury: '+str(self.beta_gi));
    
    #  Comput overall Tisue health
    #
    def describe(this):
        """
        Full description of Tissue.

        Returns
        -------
        None.

        """
        this.info();
        
        print('------')
        print('HEALTH')
        print('IRI: ' + str(this.iri))
        print('DTI: ' + str(this.dpi))
        print('GI : '+ str(this.gi))
        
        print ('Health: '+str(this.health()));
        
 
        
