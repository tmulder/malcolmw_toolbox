from Tkinter import *

import sys
import os

sys.path.append(os.environ['MW_SRC'] + '/GUI')

import PlotEventsPerTimeGUI as ept

class InitMenu:
	def __init__(self,master):
		frame = Frame(master)
		frame.pack()
		bwid = 30
        
		btxtcmd = [("Plot Events per Unit Time",self.events_per_time),("Plot Gutenberg-Richter Relationship",self.empty),("Plot Omori's Law",self.empty)]
		i=0
		for t in btxtcmd:
			button = Button(frame,text=t[0],command=t[1],width=bwid)
			button.grid(row=i)
            		i+=1

		button = Button(frame,text="QUIT ALL",command=master.destroy)
		button.grid(row=i)
    
	def events_per_time(self):
		child = Tk()
		ept.PlotEventsPerTimeGUI(child)

	def empty(self):
		return 0
