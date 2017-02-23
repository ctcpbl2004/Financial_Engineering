# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 10:27:40 2017

@author: Raymond
"""

import numpy as np
import scipy
from scipy.stats import norm

def Balck_Scholes(S,K,r,t,sigma):
    S = float(S)
    K = float(K)
    r = float(r)
    sigma = float(sigma)
    t = float(t)/250.     #unit of t is days of maturity, which include holidays.
    
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*t)/(sigma*np.sqrt(t))
    d2 = d1 - sigma*np.sqrt(t)
    
    nd1 = norm.cdf(d1)
    nd2 = norm.cdf(d2)
    
    Call = S* nd1 - K * np.exp(-r*t) * nd2
    Put = S* (nd1 - 1.) - K * np.exp(-r*t) * (nd2 - 1)
    return Call,Put        


def Futures_Option(S,K,r,t,sigma):
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
        
        
print Balck_Scholes(S = 9780,K = 9800,r = 0.0125,t = 5,sigma = 0.0687)

print Futures_Option(S = 9780,K = 9800,r = 0.0125,t = 5,sigma = 0.0687)









