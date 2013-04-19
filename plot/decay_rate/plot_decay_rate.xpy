import matplotlib.pyplot as plt

import argparse

from math import log

import numpy as np

#input_file = "/home/malcolm/dropbox/SSA/decay_rate/magnitude_times.txt"
#output_file = "/home/malcolm/dropbox/SSA/decay_rate/GR_plot.png"

def readfile(path):
	infile = open( path, "r" )

	magnitude, t = [],[]

	for line in infile:
		l = line.split()
		magnitude.append(float(l[0]))
		t.append(float(l[1]))
	return t, magnitude

def plot_gutenberg_richter(mag):
	BIN_WIDTH = 0.1
	COMPLETENESS_LB = 4.0
	COMPLETENESS_UB = 6.3
	EXTRAP_LB = 1.0
	EXTRAP_UB = 9.0

	count = {}
	for i in np.arange(-1.0,10.0, BIN_WIDTH):
		count[i] = 0

	for m in mag:
		for key in count:
			if m > key-(BIN_WIDTH/2) and m <= key+(BIN_WIDTH/2): count[key] += 1

	N=len(mag)
	count_max = max([ count[key] for key in count ])

	bins = sorted(count)
	nevents = [ count[x] for x in bins ]
	bin_left = [ x-(BIN_WIDTH/2) for x in bins ]

	x_to_fit, y_to_fit = [],[]
	for bin in bins:
		if bin > COMPLETENESS_LB and bin <= COMPLETENESS_UB:
			x_to_fit.append(bin)
			y_to_fit.append(log(count[bin],10)) if not count[bin] == 0 else y_to_fit.append(0)
			
	b,a = np.polyfit(x_to_fit, y_to_fit, 1)
	b=abs(b)

	def gr_reln(m):
		return 10**(a-b*m)

	line = [gr_reln(x) for x in np.arange(COMPLETENESS_LB,COMPLETENESS_UB,0.1)]
	extrap_domain = [x for x in list(np.arange(EXTRAP_LB, COMPLETENESS_LB, BIN_WIDTH))+list(np.arange(COMPLETENESS_UB, EXTRAP_UB, BIN_WIDTH))]
	line_extrap = [gr_reln(x) for x in extrap_domain]

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_title( "Haida Gwaii Aftershock Sequence: Gutenberg-Richter Relationship" )
	ax.bar( bin_left, nevents, width=BIN_WIDTH, log=True )
	ax.plot( np.arange(COMPLETENESS_LB,COMPLETENESS_UB,0.1), line, "r" )
	ax.plot( extrap_domain, line_extrap, "r--" )
	ax.set_xlabel( "Magnitude" )
	#ax.set_xticks( np.arange(-1.0,10.0,BIN_WIDTH) )
	ax.set_yscale("log")
	ax.set_ylabel( "Event count" )
	ax.text( 6.0, 0.9*count_max, "a=%.3f, b=%.3f" % (a,b) )

def plot_omori(t,mag):
	D_LEN = 24*60*60	#number of seconds in a day
	BIN_WIDTH = 1.0		#bin width in days
	K = 7.8
	t_max = max(t)

	count = {}
	
	for time in np.arange(0, t_max+BIN_WIDTH, BIN_WIDTH):
		count[time] = 0

	for time in t:
		for key in count:
			if time > key-(BIN_WIDTH/2) and time <= key+(BIN_WIDTH/2): count[key]+=1

	bins = sorted(count)
	nevents = [ count[x] for x in bins ]
	bin_left = [ x-(BIN_WIDTH/2) for x in bins ]

	def omori_curve(p,t):
		#return 500/((0.05 + t)**p) if t>0 else count[0.0]
		return 500/((0.05 + t)**p)

	p = calc_p( count, K )
	p=1.0

	best_curve = [omori_curve(p,time) for time in bins]
	curve1 = [omori_curve(0.5,time) for time in bins]
	curve2 = [omori_curve(1.0,time) for time in bins]
	curve3 = [omori_curve(1.5,time) for time in bins]

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_title( "Haida Gwaii Aftershock Sequence: Omori's Law" )
	ax.bar( bin_left, nevents, width=BIN_WIDTH )
	#ax.plot( bins, best_curve, "r")

	ax.plot( bins, curve1, "r")
	ax.plot( bins, curve2, "r")
	ax.plot( bins, curve3, "r")

	ax.set_xlabel( "Days since main shock" )
	ax.set_xlim( -1, max(bins)+1 )
	ax.set_ylabel( "Event count" )
	ax.set_ylim( 0, 500 )

def calc_p( count, K):	
	t_pts = [ 4.0, 20.0, 25.0, 30.0 ]
	p = []

	for time in t_pts:
		p.append(log((K/count[time]),time))

	return sum(p)/len(p)

parser = argparse.ArgumentParser(description="Plot GR Relation and modified Omori's Law.")
parser.add_argument('input_file',metavar='infile',type=str,nargs=1,\
		help = "Input file")
parser.add_argument('output_file',metavar='outfile',type=str,nargs=1,\
		help = "Output file")
args = parser.parse_args()


t,mag = readfile(args.input_file[0])

#plot_gutenberg_richter(mag)

plot_omori(t,mag)

#ax2 = fig.add_subplot(212)
#ax2.plot(t,mag,"ko")
#ax2.set_xlabel( "Days since main shock" )
#ax2.set_ylabel( "Magnitude" )
plt.savefig(args.output_file[0])
plt.show()
