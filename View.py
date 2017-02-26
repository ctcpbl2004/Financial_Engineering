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
import pandas as pd
from Model import Futures_Option,Maturity
import Controller

class GUI(tk.Tk):
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_title('Title')
        self.root.geometry('1450x600')
        #self.root.iconbitmap('Icon.ico')
        
        self.fig = Figure(figsize=(6,4), dpi=120)
        self.fig.set_tight_layout(True)
        self.fig.patch.set_facecolor('#181818')
        
        self.Stock_Chart = self.fig.add_subplot(111,axisbg='#213139')
        self.Stock_Chart.tick_params(axis='both', which='major', labelsize=8)
        self.Stock_Chart.set_xlabel('Simulation Time', fontsize=10)
        self.Stock_Chart.set_ylabel('Stock price', fontsize=10)
        
        self.Stock_Chart.tick_params(axis='both', which='major',colors='white', labelsize=6)
        self.Stock_Chart.spines['bottom'].set_color('white')
        self.Stock_Chart.spines['top'].set_color('white')
        self.Stock_Chart.spines['left'].set_color('white')
        self.Stock_Chart.spines['right'].set_color('white')
        self.Stock_Chart.xaxis.label.set_color('white')
        self.Stock_Chart.yaxis.label.set_color('white')
        
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().place(x=10,y=10)
        self.canvas.get_tk_widget().configure(background='#181818',  highlightcolor='#181818', highlightbackground='#181818')

        self.Button = ttk.Button(self.root, text = 'Click', command = self.Payoff_Graph)
        self.Button.place(x=500,y=500)

        
        self.Tree_table = ttk.Treeview(self.root,height="7",selectmode='none')

        self.Tree_table["columns"]=("column1","column2",'column3','column4','column5','column6','column7','column8')
        self.Tree_table.column("#0",width=40, anchor='center')
        self.Tree_table.column("column1", width=80, anchor='center' )
        self.Tree_table.column("column2", width=60, anchor='center')
        self.Tree_table.column("column3", width=80 , anchor='center')
        self.Tree_table.column("column4", width=80, anchor='center' )
        self.Tree_table.column("column5", width=60, anchor='center')
        self.Tree_table.column("column6", width=80 , anchor='center')
        self.Tree_table.column("column7", width=60, anchor='center')
        self.Tree_table.column("column8", width=120 , anchor='center')


        self.Tree_table.heading('#0', text='')
        self.Tree_table.heading("column1", text="Buy/Sell")
        self.Tree_table.heading("column2", text="Call/Put")
        self.Tree_table.heading("column3", text="Contract")
        self.Tree_table.heading("column4", text="Exercise")
        self.Tree_table.heading("column5", text="Premium")
        self.Tree_table.heading("column6", text="Quantity")
        self.Tree_table.heading("column7", text="Maturity")
        self.Tree_table.heading("column8", text="Implied Vol")
        self.Tree_table.tag_configure('oddrow', background='black',foreground = 'white')

        self.Tree_table.place(x=750, y=10)

        Style = ttk.Style()
        Style.configure(".", font=('Helvetica', 8), foreground="white")
        Style.configure("Treeview", foreground='white')
        Style.configure("Treeview", background='#181818')
        Style.configure("Treeview.Heading", foreground='black')
        Style.configure("TButton", foreground='black')
        Style.configure("TButton", background='#181818')

        self.Portfolio = self.Options_Portfolio(S = 9750.47,Percent_Change = 0.02,Holding_days = 3.,r = 0.0125)


        for i in range(len(self.Portfolio[0]['Buy/Sell'])):
            self.Tree_table.insert("",i,text=str(i+1),values=(self.Portfolio[0]['Buy/Sell'][i],
                                                           self.Portfolio[0]['Call/Put'][i],
                                                            self.Portfolio[0]['Contract'][i],
                                                            self.Portfolio[0]['Exercise'][i],
                                                            self.Portfolio[0]['Current_Premium'][i],
                                                            self.Portfolio[0]['Quantity'][i],
                                                            self.Portfolio[0]['Maturity'][i],
                                                            str(round(self.Portfolio[0]['Implied_Vol'][i]*100.,2)) + '%'))


        self.Payoff_Graph()



        self.root.configure(background='#181818')
        self.root.mainloop()


    def Graph(self):
        self.Stock_Chart.clear()
        self.Stock_Chart.plot( range(100),np.random.lognormal(size = 100) ,lw=1,color='#01485E',alpha=0.5)
        self.canvas.show()



    def Payoff_Graph(self):
        self.Stock_Chart.clear()
        self.Stock_Chart.plot(self.Portfolio[1].index,self.Portfolio[1],lw = 1, color = 'white')
        self.Stock_Chart.fill_between(self.Portfolio[1].index,0,self.Portfolio[1],facecolor = '#107B8C')
        self.Stock_Chart.grid(True,color='white')
        self.canvas.show()

#107B8C
#3CA9C8





    def Save_Reload(self):
        pass







    def Options_Portfolio(self,S,Percent_Change,Holding_days,r):
        Position = Controller.Controller.Position_Query()
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
        return Position,Simulation['Total_Profit']

if __name__ == "__main__":
    app = GUI()
    



