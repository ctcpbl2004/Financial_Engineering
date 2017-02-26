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
pd.options.mode.chained_assignment = None

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


class Maturity(object):
    @staticmethod
    def Monthly_Contract(Contract):
        Today = datetime.datetime.today()
        Date = datetime.datetime.strptime(str(Contract), '%Y%m')
        n = 0
        
        for i in range(1,30):
            if Date.weekday() == 2:
                n = n + 1        
                if n == 3:
                    return Date.strftime('%Y-%m-%d'),np.busday_count(Today,Date) + 1
    
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
                    return Date.strftime('%Y-%m-%d'),np.busday_count(Today,Date) + 1
                
                Date = Date + datetime.timedelta(days = 1)
            else:
                
                Date = Date + datetime.timedelta(days = 1)


#==============================================================================
'''
Pricing(S,K,r,t,sigma)
Implied_Vol_Call(Premium,S,K,r,t)
Implied_Vol_Put(Premium,S,K,r,t)
'''

def Options_Portfolio(S,Percent_Change,Holding_days,r):
    r = 0.0125
    S = 9750.47
    Percent_Change = 0.02
    Holding_days = 3.
    
    
    
    Position = Controller.Position_Query()
    Position['Maturity'] = np.nan
    Position['Implied_Vol'] = np.nan
    
    for i in range(len(Position)):
        if len(Position['Contract'][i].split('W')) == 2:
            Position['Maturity'][i] = Maturity.Weekly_Contract(Position['Contract'][i])[1]
        else:
            Position['Maturity'][i] = Maturity.Monthly_Contract(Position['Contract'][i])[1]
    
    for i in range(len(Position)):
        if Position['Call/Put'][i] == 'Call':
            Position['Implied_Vol'][i] = Futures_Option.Implied_Vol_Call(Position['Current_Premium'][i],S,Position['Exercise'][i],r,Position['Maturity'][i])
        else:
            Position['Implied_Vol'][i] = Futures_Option.Implied_Vol_Put(Position['Current_Premium'][i],S,Position['Exercise'][i],r,Position['Maturity'][i])
    
    
    Simulation_index = range(int(S * (1 - Percent_Change)),int(S * (1 + Percent_Change) ))
    Simulation = pd.DataFrame(index = Simulation_index,columns = Position.index)
    
    for Pos in Simulation.columns:
        if Position['Call/Put'][Pos] == 'Call':
            if Position['Buy/Sell'][Pos] == 'Buy':
                for S in Simulation.index:
                        Simulation[Pos][S] = Futures_Option.Pricing(S,Position['Exercise'][Pos],r,Position['Maturity'][Pos] - Holding_days,Position['Implied_Vol'][Pos])[0] - Position['Current_Premium'][Pos]
            else:
                for S in Simulation.index:
                        Simulation[Pos][S] =  Position['Current_Premium'][Pos] - Futures_Option.Pricing(S,Position['Exercise'][Pos],r,Position['Maturity'][Pos] - Holding_days,Position['Implied_Vol'][Pos])[0]
        else:
            if Position['Buy/Sell'][Pos] == 'Buy':
                for S in Simulation.index:
                        Simulation[Pos][S] = Futures_Option.Pricing(S,Position['Exercise'][Pos],r,Position['Maturity'][Pos] - Holding_days,Position['Implied_Vol'][Pos])[1] - Position['Current_Premium'][Pos]
            else:
                for S in Simulation.index:
                        Simulation[Pos][S] =  Position['Current_Premium'][Pos] - Futures_Option.Pricing(S,Position['Exercise'][Pos],r,Position['Maturity'][Pos] - Holding_days,Position['Implied_Vol'][Pos])[1]
    
    
    Simulation = Simulation.fillna(method = 'ffill')
    
    Simulation['Total_Profit'] = Simulation.sum(axis = 1)
    Simulation['Zero_axis'] = 0.
    
    
    Breakeven = []
    
    for i in Simulation.index[1:-2]:
        if Simulation['Total_Profit'][i] * Simulation['Total_Profit'][i-1] <= 0.:
            Breakeven.append(i)
        else:
            pass
        
            
    print 'Breakeven point = ',Breakeven
    
    fig,ax = plt.subplots(1,1)
    ax.fill_between(Simulation.index,0,Simulation['Total_Profit'], facecolor='green', alpha=0.5)
    plt.show()


































