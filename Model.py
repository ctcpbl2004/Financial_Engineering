# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 15:53:52 2017

@author: Raymond
"""

from Controller import Controller
import pandas as pd
import numpy as np
import sys
import warnings
import matplotlib.pyplot as plt
import datetime
warnings.simplefilter(action = 'ignore', category = FutureWarning)
warnings.simplefilter(action = 'ignore', category = DeprecationWarning)
from scipy.stats import norm
reload(sys)
sys.setdefaultencoding('utf8')


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




class Maturity():
    @staticmethod
    def Monthly_Contract(Contract):
        Today = datetime.datetime.today()
        Date = datetime.datetime.strptime(str(Contract), '%Y%m')
        n = 0
        
        for i in range(1,30):
            if Date.weekday() == 2:
                n = n + 1        
                if n == 3:
                    return Date.strftime('%Y-%m-%d'),np.busday_count(Today,Date)
    
                    break
                else:
                    pass
                
                Date = Date + datetime.timedelta(days = 1)
        
            else:
                Date = Date + datetime.timedelta(days = 1)        
    
    @staticmethod
    def Weekly_Contract(Contract):
        Today = datetime.datetime.today()
        Date = datetime.datetime.strptime(str(Contract.split('W')[0]),'%Y%m')
        Week = int(Contract.split('W')[1])
        
        n = 0
        for i in range(1,30):
            if Date.weekday() == 2:
                n = n + 1
                if n == Week:
                    return Date.strftime('%Y-%m-%d'),np.busday_count(Today,Date)
                
                Date = Date + datetime.timedelta(days = 1)
            else:
                
                Date = Date + datetime.timedelta(days = 1)






















