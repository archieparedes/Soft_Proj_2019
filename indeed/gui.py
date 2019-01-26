"""
@author Archie_Paredes
@created JAN 26, 2018
@version 1.0
Indeed API GUI
"""

import os
from tkinter import *
from indeed_api import *

class ui(Tk):
    def __init__(self,parent=None):
        Tk.__init__(self,parent)
        self.title(' Data Science Jobs ')
        self.make_widgets()
    def calc_reponse(self):
        print(str(self.loc.get()))
    def make_widgets(self):
        Label(self, text='Search Location:',width=40).pack()
        self.loc = Entry(self, width = 40)
        self.loc.pack()
        Button(self,text='Submit', command=lambda:self.calc_reponse()).pack(side = BOTTOM)
                
ui().mainloop()
