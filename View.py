# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 17:38:17 2017

@author: Raymond
"""

import Tkinter as tk
import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class GUI(tk.Tk):
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_title('Title')
        self.root.geometry('800x600')
        #self.root.iconbitmap('Icon.ico')
        
        self.fig = Figure(figsize=(6,4), dpi=120)
        self.fig.set_tight_layout(True)
        self.fig.patch.set_facecolor('#FFFFFF')
        
        self.Stock_Chart = self.fig.add_subplot(111,axisbg='#FFFFFF')
        self.Stock_Chart.tick_params(axis='both', which='major', labelsize=8)
        self.Stock_Chart.set_xlabel('Simulation Time', fontsize=10)
        self.Stock_Chart.set_ylabel('Stock price', fontsize=10)
        
        self.Stock_Chart.tick_params(axis='both', which='major',colors='black', labelsize=6)
        self.Stock_Chart.spines['bottom'].set_color('black')
        self.Stock_Chart.spines['top'].set_color('black')
        self.Stock_Chart.spines['left'].set_color('black')
        self.Stock_Chart.spines['right'].set_color('black')
        self.Stock_Chart.xaxis.label.set_color('black')
        self.Stock_Chart.yaxis.label.set_color('black')
        
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().place(x=10,y=10)
        self.canvas.get_tk_widget().configure(background='#000000',  highlightcolor='#FFFFFF', highlightbackground='#FFFFFF')

        self.Button = ttk.Button(self.root, text = 'Click', command = self.Graph)
        self.Button.place(x=500,y=500)
        
        self.Graph()
        
        self.root.mainloop()


    def Graph(self):
        self.Stock_Chart.clear()
        self.Stock_Chart.plot( range(100),np.random.lognormal(size = 100) ,lw=1,color='#01485E',alpha=0.5)
        self.canvas.show()


if __name__ == "__main__":
    app = GUI()
    



