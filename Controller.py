# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 14:38:25 2017

@author: Raymond
"""

import sqlite3
import pandas as pd
import numpy as np
import sys
import datetime

class Controller(object):
    @staticmethod
    def Position_Query(): #Controller.Position_Query()
        connection = sqlite3.connect("Position.db")
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Options_Position ")
        
        data = cursor.fetchall()
        connection.close()            

        df = pd.DataFrame(columns = ['Buy/Sell','Call/Put','Contract','Exercise','Current_Premium','Quantity'],index = range(100))
        
        for i in range(len(data)):
            df.ix[i] = data[i]
        
        df = df.dropna()
        return df


    @staticmethod
    def Position_insert(NewPosition): #Controller.Position_insert(NewPosition=(1,2,3,4,5,6))
        connection = sqlite3.connect("Position.db")
        
        cursor = connection.cursor()
        sys.stderr.write("[info] executing sql for writing data to db \n")
                
        cursor.execute("INSERT  INTO Options_Position VALUES (?,?,?,?,?,?)",(NewPosition))

        connection.commit()
        connection.close()




