# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 10:00:11 2017

@author: Raymond
"""

import datetime
import numpy as np
import pandas as pd
'''
0: Mon
1: Tue
2: Wed
3: Thu
4: Fri
5: Sat
6: Sun
'''


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

    #return Date,Week
#==============================================================================
            


print Weekly_Contract('201704W1')
