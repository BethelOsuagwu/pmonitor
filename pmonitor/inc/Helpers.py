# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 19:02:55 2021

@author: Bethel Osuagwu
"""
import math;
class Helpers:
    
    @staticmethod
    def linearBeta(t,dt):
        """
        Calculate the linear decay/relief rate. Essentially the same as gradient 
        in line equation.

        Parameters
        ----------
        t : float
            The time in seconds it should take for an effect to relieve to zero.
        dt : float
            Sampling time in seconds. The default is 1.

        Returns
        -------
        float
            The linear decay/relief rate.

        """
        
        return dt/t;
    
    @staticmethod
    def beta(t,dt):
        """
        Calculate the exponential decay/relief rate. Essentially the same as alpha in 
        exponentially weighted moving averrage filter.

        Parameters
        ----------
        t : float
            The time in seconds it should take for an effect to relieve to zero.
        dt : float
            Sampling time in seconds. The default is 1.

        Returns
        -------
        float
            The decay/relief rate.

        """
        
        return 1-math.e**(-5*dt/t);
    
    @staticmethod
    def tau(beta,dt=1):
        """
        Compute the exponential time constant.
        
        Parameters
        ----------
        beta : float
            The decay/relief rate.
        dt : float
            Sampling time in seconds. The default is 1.
            
        Returns
        -------
        float
            The time constant
        """
        
        # Avoid log of 0
        if(beta==1):
            beta=0.999;
        
        return -dt/(math.log(1-beta));        
        
    @classmethod
    def impulseResponse(cls,beta,dt=1,show=True):
        """
        Exponential decay Impulse response of the monitoring filter.

        Parameters
        ----------
        beta : float
            The decay/relief rate.
        dt : float
            Sampling time in seconds. The default is 1.
        show : boolean
            If true the response will be ploted.
            
        Returns
        -------
        List
            A 2d list where the first row contains response and the second row 
            is time

        """
        
        
        
        # Calc tau
        tau=cls.tau(beta,dt);
        
       
        # Decay to zero in 5 taus
        t=5*tau;
        
        # Get number of samples needed to decay to zero
        N=round(t/dt);
        
        
        # Unit step function
        u=1;# we will just repeate it
        
        hs=[];
        ts=[];
        for n in range(0,N):
            hn=(beta+1)*((1-beta)**n)*u
            hs.append(hn);
            ts.append(n*dt);
        
        
        
        if(show):
            import matplotlib.pyplot as plt;
            plt.plot(ts,hs)
            plt.title('Impulse response');
            plt.xlabel('Time (s)');
            plt.ylabel('Amplitude');
        
        
        return [hs,ts];
    
    @staticmethod
    def imp():
        # This is a temporary test code
        a=0.00166;
        d=0.01;
        dt=d;
        
        # Get number of samples needed to decay to zero
        N=30;
        
        show=True;
        
        # Unit step function
        u=1;# we will just repeate it
        
        hs=[];
        ts=[];
        for n in range(0,N):
            hn=((a**2+d)*(1-a)**(n-1))/d
            #hn=(beta+1)*((1-beta)**n)*u
            hs.append(hn);
            ts.append(n*dt);
        
        
        
        if(show):
            import matplotlib.pyplot as plt;
            plt.plot(ts,hs)
            plt.title('Impulse response');
            plt.xlabel('Time (s)');
            plt.ylabel('Amplitude');
        
        
        
        
        
    
    