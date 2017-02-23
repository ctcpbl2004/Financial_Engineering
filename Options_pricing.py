# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 10:27:40 2017

@author: Raymond
"""

import numpy as np
import scipy
from scipy.stats import norm
import timeit
import pandas as pd

        

class Futures_Option(object):
    @staticmethod
    def Pricing(S,K,r,t,sigma):
        S = float(S)
        K = float(K)
        r = float(r)
        sigma = float(sigma)
        t = float(t)/250.     #unit of t is days of maturity, which include holidays.
        
        d1 = (np.log(S/K) + (r + 0.5*sigma**2)*t)/(sigma*np.sqrt(t))
        d2 = d1 - sigma*np.sqrt(t)
        
        nd1 = norm.cdf(d1)
        nd2 = norm.cdf(d2)
        
        Call = S * np.exp(-r*t) * nd1 - K * np.exp(-r*t) * nd2
        Put = S * np.exp(-r*t) * (nd1 - 1.) - K * np.exp(-r*t) * (nd2 - 1)
        return Call,Put        
    
    @staticmethod
    def Implied_Vol_Call(Premium,S,K,r,t):
        accuracy = 0.0000001
        Low_bound = 0.
        Up_bound = 1.
        
        if (Futures_Option.Pricing(S,K,r,t,Low_bound)[0] - Premium) * (Futures_Option.Pricing(S,K,r,t,Up_bound)[0] - Premium) < 0.:

            while (Up_bound - Low_bound)/2. >= accuracy:
                Mid = (Low_bound + Up_bound)/2.
                #print (Black_Scholes_Pricing.Pricing(S,K,r,t,Mid)[0] - Premium),(Black_Scholes_Pricing.Pricing(S,K,r,t,Up_bound)[0] - Premium)
                if (Futures_Option.Pricing(S,K,r,t,Mid)[0] - Premium) * (Futures_Option.Pricing(S,K,r,t,Low_bound)[0] - Premium) < 0.:
                    Up_bound = Mid
                    
                elif (Futures_Option.Pricing(S,K,r,t,Mid)[0] - Premium) * (Futures_Option.Pricing(S,K,r,t,Up_bound)[0] - Premium) < 0.:
                    Low_bound = Mid
                else:
                    Up_bound = Mid
                    Low_bound = Mid

            
            ImpVol = (Low_bound + Up_bound)/2.
            return ImpVol
        else:
            raise Exception('Error!Please choose a interval where the Error change its signs')

    @staticmethod
    def Implied_Vol_Put(Premium,S,K,r,t):
        accuracy = 0.00001
        Low_bound = 0.
        Up_bound = 1.
        
        if (Futures_Option.Pricing(S,K,r,t,Low_bound)[1] - Premium) * (Futures_Option.Pricing(S,K,r,t,Up_bound)[1] - Premium) < 0.:

            while (Up_bound - Low_bound)/2. >= accuracy:
                Mid = (Low_bound + Up_bound)/2.
                #print (Black_Scholes_Pricing.Pricing(S,K,r,t,Mid)[0] - Premium),(Black_Scholes_Pricing.Pricing(S,K,r,t,Up_bound)[0] - Premium)
                if (Futures_Option.Pricing(S,K,r,t,Mid)[1] - Premium) * (Futures_Option.Pricing(S,K,r,t,Low_bound)[1] - Premium) < 0.:
                    Up_bound = Mid
                    
                elif (Futures_Option.Pricing(S,K,r,t,Mid)[1] - Premium) * (Futures_Option.Pricing(S,K,r,t,Up_bound)[1] - Premium) < 0.:
                    Low_bound = Mid
                else:
                    Up_bound = Mid
                    Low_bound = Mid

            
            ImpVol = (Low_bound + Up_bound)/2.
            return ImpVol
        else:
            raise Exception('Error!Please choose a interval where the Error change its signs')

#================================================================================================================================================

['Sell','Call','201704',31,2]

Vol = Futures_Option.Implied_Vol_Call(48.5,9769,9750,0.0125,5)


S = 9769.
PercentChange = 0.05
t = 5
df = pd.DataFrame(index = range(int(S * (1. - PercentChange)),int(S * (1. + PercentChange))),columns = range(t))

for S in df.index:
    for t in df.columns:
        df[t][S] = 48.5 - Futures_Option.Pricing(S,9750,0.0125,t,Vol)[0]
        
        



print df
df.plot()


