from Tkinter import *

import os

class PlotEventsPerTimeGUI:
	def __init__(self,master):
		print "INIT"
		frame = Frame(master)
		frame.pack()

		label = Label(frame, text="Input file: ")
        	label.grid(row=1,column=1)
        
	        self.text1 = Text(frame,width=100,height=1)
	        self.text1.insert(1.0,"~/dropbox/mag_times.txt")
	        self.text1.grid(row=1,column=2)

		button = Button(frame,text="Plot",command=self.plot)
		button.grid(row=1,column=3)

	def plot(self):
		infile = self.text1.get(1.0,END).rstrip('\n')
		os.system( "plot_events_per_time " + infile )
