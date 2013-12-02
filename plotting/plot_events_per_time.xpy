import matplotlib.pyplot as plt
import numpy as np
import argparse
from math import log
from antelope.datascope import *


def read_data(path):
        """Read data from Antelope database."""
        #Open db
        dbin = dbopen(path,"r")

        #Create appropriate view
        dbin = dbin.lookup(table="origin")
        dbin = dbin.join("event")
        dbin = dbin.subset("orid==prefor")
        dbin = dbin.join("netmag")

        #Get record count
        nrec = dbin.nrecs()

        #Read all magnitude and origin time data into lists
        #Store origin time as days since epoch
        mag = [ dbin.getv("magnitude")[0] for dbin[3] in range(nrec) ]
        time = [ dbin.getv("time")[0]/(24*60*60) for dbin[3] in range(nrec) ]

        #Remove all null magnitude values and corresponding time values
        time = [ time[i] for i in range(len(time)) if not mag[i] == -999.00 ]
        mag = [ m for m in mag if not m == -999.00 ]

        #Convert time to days since first event in db
        min_time = min(time)
        time = [ t - min_time for t in time ]

        return time,mag

def readfile(path):
        """Read data from input flat file."""

        #Open file
        infile = open( path, "r" )

        #Empty lists
        magnitude, t = [],[]

        #Read all data from flat file into lists, there should be no null magnitude values
        for line in infile:
                l = line.split()
                magnitude.append(float(l[0]))
                t.append(float(l[1]))

        return t, magnitude

def plot_events_per_time(time,mag):
	""" Generate a histogram of number of events per unit time bin """

	#Set BIN_WIDTH to default value of 1 day if no command line argument provided
	BIN_WIDTH = args.bin_width[0] if args.bin_width else 1.0

	#Get the maximum origin time
	t_max = max(time)


	#Create an array of bin boundaries
	bins = np.arange(0,t_max+BIN_WIDTH,BIN_WIDTH)
	#Get array of indices mapping each origin time to a bin
	inds = np.digitize(time,bins)

	#Find the left hand edge of each bin for plotting
	x_values = [ bin-(BIN_WIDTH/2) for bin in bins ]

	#Initialize an array of zeros corresponding with length corresponding to number of bins
	y_values = np.zeros(len(x_values))
	#Perform count of # of events in each bin
	for ind in inds: y_values[ind-1] += 1

	#Plot data
	##########
	#Create figure
	fig = plt.figure()
	#Add a subplot
	ax = fig.add_subplot(111)

	#Plot bars, don't forget to plot bars logarithmically if necessary
	ax.bar(x_values,y_values,width=BIN_WIDTH,log=True) if args.log_y_scale else ax.bar(x_values,y_values,width=BIN_WIDTH)
	#Plot Omori's law decay curve?
	if args.omori_params:
		A,p = args.omori_params[0],args.omori_params[1]
		curve_x = [ x for x in x_values ]
		curve_y = [ A*(1-p)*pow(x,-p) for x in x_values ]
		ax.plot(curve_x,curve_y,"r")

	#Reconstruct title/axes labels from command line arguments if necessary
	if args.title:
		title = ''
		for s in args.title: title += "%s " % s
	if args.x_label:
		x_label = ''
		for s in args.x_label: x_label += "%s " % s
	if args.y_label:
		y_label=''
		for s in args.y_label: y_label += "%s " % s
	#Label plot/axes
	ax.set_title(title) if args.title else ax.set_title( "Number of events per " + str(BIN_WIDTH) + " day(s)" )
	ax.set_xlabel(x_label) if args.x_label else ax.set_xlabel( "Time [days]" )
	ax.set_ylabel(y_label) if args.y_label else ax.set_ylabel( "Number of events [count]" )

	#Scale y-axis logarithmically?
	if args.log_y_scale: ax.set_yscale('log')

	#Set plot domain and/or range?
	ax.set_xlim(args.xlim[0],args.xlim[1]) if args.xlim else ax.set_xlim(min(x_values)-5, max(x_values)+5)
	if args.ylim: ax.set_ylim(args.ylim[0],args.ylim[1])

	
		

#####
#MAIN
#####

#Parse command line options
parser = argparse.ArgumentParser(description="Plot number of events per unit time.")
parser.add_argument('input',metavar='input',type=str,nargs=1,\
                help = "Input database (Alternatively, input flat file and specify -ff option.)")

parser.add_argument('-s',dest='output_file',nargs=1,help='Save output to specified file' )
parser.add_argument('-b',dest='bin_width',nargs=1,type=float,help='Define bin width in # of days. Defaults to 1.')
parser.add_argument('-t',dest='title',nargs='+',type=str,help='Plot title.')
parser.add_argument('-x',dest='x_label',nargs='+',type=str,help='X-axis label')
parser.add_argument('-y',dest='y_label',nargs='+',type=str,help='Y-axis label')
parser.add_argument('-xlim',dest='xlim',nargs=2,type=float,help='Plot domain')
parser.add_argument('-ylim',dest='ylim',nargs=2,type=float,help='Plot range')
parser.add_argument('-o',dest='omori_params',nargs=2,type=float,help="Omori's law parameters A and p")

parser.add_argument('-ly','--log_y_scale',action='store_true',help='Scale y-axis logarithmically')
parser.add_argument('-ff','--flat_file_input',action='store_true',help='Input is flat file, not Antelope database.')


args = parser.parse_args()

#Read data from input file or database as appropriate
if args.flat_file_input: time,mag = readfile(args.input[0])
else: time,mag = read_data(args.input[0])

#Generate plot
plot_events_per_time(time,mag)

#Save figure?
if args.output_file: plt.savefig(args.output_file[0] + '.png')

#Show figure
plt.show()

