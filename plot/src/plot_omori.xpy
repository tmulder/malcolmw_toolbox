import matplotlib.pyplot as plt

import argparse

from math import log,pow

import numpy as np

def readfile(path):
	""" Read data from input file """

        infile = open( path, "r" )

        magnitude, t = [],[]

        for line in infile:
                l = line.split()
                magnitude.append(float(l[0]))
                t.append(float(l[1]))
        return t, magnitude


def plot_omori(time,mag):
	"""Generate cumulative number of events as function of time plot. Fit Omori's law curve if -f option specified."""

	#Get sample spacing from command line arguments or set to default
	X_INT = args.x_int[0] if args.x_int else 1.0

	#Get the maximum origin time
        t_max = max(time)

	#Create bins of X_INT width
	bins = np.arange(0,t_max+X_INT,X_INT)

	#Bin events
	count = np.zeros(len(bins))
	inds = np.digitize(time,bins)
	for i in inds:
		count[i-1] += 1

	#Perform a cumulative count of events in each bin
	cum_count = count.cumsum()

	x_values = [ b for b in bins ]
	y_values = [ c for c in cum_count ]


	#Plot data
	##########
	#Create figure
	fig = plt.figure()
	#Add a subplot
	ax = fig.add_subplot(111)

	ax.plot(x_values,y_values,"bo")

	#Determine constants to Omori's law, if -f option specified
	# N(t) = A*t^(1-p)
	# N(t) = A*t^m
	if args.fit_data:
		A,m = fit_data(x_values,y_values)
		curve_x = x_values
		curve_y = [ A*pow(x,m) for x in x_values ]
		ax.plot(curve_x,curve_y,"r")
		#Display fit parameters?
		if args.display_fit_parameters: ax.text(0.1*max(x_values),0.9*max(y_values),"N(t) = A*t^(1-p)\nA = %.3f\np = %.3f" % (A,abs(m-1)))

	#Reconstruct title/axes labels from command line arguments if necessary
	if args.title:
		#print args.title
		title = ''
		for s in args.title: title += "%s " % s
	if args.x_label:
		x_label = ''
		for s in args.x_label: x_label += "%s " % s
	if args.y_label:
		y_label = ''
		for s in args.y_label: y_label += "%s " % s

	#Label plot/axes
	ax.set_title(title) if args.title else ax.set_title("Cumulative Event Count vs. Time")
	ax.set_xlabel(x_label) if args.x_label else ax.set_xlabel("Time [days]")
	ax.set_ylabel(y_label) if args.y_label else ax.set_ylabel("Cumulative Event Count [count]")

	#Scale axes logarithmically?
	if args.log_log_scale:
		ax.set_xscale('log')
		ax.set_yscale('log')

def fit_data(x_values,y_values):
	"""Find the line which best fits log(x_values) and log(y_values) in the Least Squares sense."""

	#Are any gaps specified through -g option?
	GAPS = args.gaps if args.gaps else None

	#If no gap end is specified for the last specified gap start, assume gap goes to end of dataset.
	if not GAPS == None and not len(GAPS)%2 == 0:
		GAPS.append(x_values[-1])

	#Remove all falling within data gaps
	while not GAPS == None and not len(GAPS) == 0:
		GAP_START,GAP_END = GAPS.pop(0), GAPS.pop(0)
		y_values = [ y_values[i] for i in range(len(x_values)) if not (x_values[i] >= GAP_START and x_values[i] <= GAP_END) ]
		x_values = [ x_values[i] for i in range(len(x_values)) if not (x_values[i] >= GAP_START and x_values[i] <= GAP_END) ]

	#Take log of x and y values
	log_x = [ log(x,10) if not x==0 else 0 for x in x_values ]
	log_y = [ log(y,10) if not y==0 else 0 for y in y_values ]

	#Fit a line to log(x) and log(y)
	slope,intercept = np.polyfit(log_x,log_y,1)

	#Calculate A from Omori's law
	# N(t) = A*t^(1-p)
	A = pow(10,intercept)
	
	#Return A, (1-p)
	return A,slope

#####
#MAIN
#####

#Parse command line options
parser = argparse.ArgumentParser(description="Plot Omori's Law.")

parser.add_argument('input_file',metavar='infile',type=str,nargs=1,\
                help = "Input file")

parser.add_argument('-s',dest='output_file',nargs=1,help='Save output to specified file.')
parser.add_argument('-xint',dest='x_int',nargs=1,type=float,help='X interval (sample spacing) in number of days.')
parser.add_argument('-g',dest='gaps',nargs='+',type=float,help='Specify gaps over which to ignore data when curve fitting. Specify as GAP_START [GAP_END [GAP_START...]] in decimal days.')
parser.add_argument('-t',dest='title',nargs='+',type=str,help='Plot title.')
parser.add_argument('-x',dest='x_label',nargs='+',type=str,help='X-axis label')
parser.add_argument('-y',dest='y_label',nargs='+',type=str,help='Y-axis label')
parser.add_argument('-xlim',dest='xlim',nargs=2,type=float,help='Plot domain.')
parser.add_argument('-ylim',dest='ylim',nargs=2,type=float,help='Plot range.')

parser.add_argument('-f','--fit_data',action='store_true',help="Fit Omori's law curve to data.")
parser.add_argument('-ll','--log_log_scale',action='store_true',help='Scale axes logarithmically.')
parser.add_argument('-d','--display_fit_parameters',action='store_true',help="Display Omori's law parameters determined by best fit.")

args = parser.parse_args()

#Read data from input file
time,mag = readfile(args.input_file[0])

#Generate plot
plot_omori(time,mag)

#Save figure?
if args.output_file: plt.savefig(args.output_file[0] + '.png')

#Show figure
plt.show()
