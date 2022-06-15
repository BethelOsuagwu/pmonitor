# -*- coding: utf-8 -*-
        
"""
Created on Tue Jul 13 20:54:03 2021

@author: Bethel Osuagwu
"""
import math;

class PressureTimeThreshold:
    
    '''
    The default parameter values were obtained from 
    doi:10.1016/j.jbiomech.2005.08.010  for a cell death threshold (Fig 4).
    See the article for the meaning of the following values.
        
    '''
    # Constants
    K=23;
    C=9;
    t0=90;
    alpha=0.15;
    
    
    def __init__(self,K=None,C=None,t0=None,alpha=None):
        """
        

        Parameters
        ----------
        K : float, optional
            Empirical constant in KPa. The default is 23KPa.
        C : float, optional
            Empirical constant in Kpa. The default is 9KPa.
        t0 : float, optional
            Empirical constant in min. The default is 90min.
        alpha : float, optional
            Epirical constant in /min. The default is 0.15/min.

        Returns
        -------
        None.

        """

        
        self.K=K or self.K;
        self.C=C or self.C;
        self.t0=t0 or self.t0;
        self.alpha=alpha or self.alpha;
        
        
        
        
    
    def timeToPressure(self,t):
        """
        

        Parameters
        ----------
        t : float
            Time, in minutes, whose related pressure will be computed.
        Params : self.pressureToTime
           

        Returns
        -------
        float.
        pressure in kPa

        """
        K=self.K;
        C=self.C;
        t0=self.t0;
        alpha=self.alpha;
        
        return K/(1+math.e**(alpha*(t-t0))) + C
    
    def pressureToTime(self,P):
        '''
        Compute the injury time threshold for the given pressure
        using equation defined in doi:10.1016/j.jbiomech.2005.08.010 .
    
    
        Parameters
        ----------
        P : float
            Pressure in KPa. self.C < P < self.C+self.K. A value of P outside 
            of this range will be compressed to fit.

    
        Returns
        -------
        [time,P_adjusted]. A 2-element list where the first is the time and the second is the adjusted pressure with respect to the limiting pressure value.
        Time in Minutes
    
        '''
        K=self.K;
        C=self.C;
        t0=self.t0;
        alpha=self.alpha;
        
        # Is P too small
        if(P==0):
            P=0.00001; # Because will get a maths error when P ==0.
            
        if(P<=self.C):
            P=self.C+P/self.C; # This is to ensure that P > C to avoid maths error.
    
        # Is P too large
        if (P>=K+C):
            P=K+C-(K+C)/P; # This is just to ensure P does not reach K+C to avoid maths error.
        
        
        #
        t=( (math.log( (K/(P-C))-1) )/alpha )+t0;
        
        return [t,P];
    
    def isDamagingPressure(self,P):
        """
        Checks if the given pressure is damaging

        Parameters
        ----------
        P : float
            Pressure in kPa.

        Returns
        -------
        boolaan

        """
        
        return P>=self.C;
    
    def isLowPressure(self,P):
        """
        Check if the given pressure is non damaging.

        Parameters
        ----------
        P : float
            Pressure in kpa.

        Returns
        -------
        boolean.

        """
        return P>self.C;

    def isHighPressure(self,P):
        """
        Check if the given pressure is excessive/instantaneosly damaging.

        Parameters
        ----------
        P : float
            Pressure in kpa.

        Returns
        -------
        boolean.

        """
        return P>=self.K+self.C;

    def getShortTermThreshold(self):
        '''
        Returns the value of pressure threshold for instantaneus damage. 

        Returns
        -------
        float
            Pressure threshold for instantaneus damage.

        '''
        return self.K+self.C;
    def getLongTermThreshold(self):
        '''
        Returns the value of pressure threshold that can only lead to damage at long time. 

        Returns
        -------
        float
            Pressure threshold for damage only after a prolonged duration.

        '''
        return self.C;