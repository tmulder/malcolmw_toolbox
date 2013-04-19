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

def plot_omori_log_log(t,mag):
	X_INT = 1.0 #plot data with sample interval 1.0 days
	GAP_START = 5
	GAP_END = 15
	count = {}

	t_max = max(t)

	for time in np.arange(1,t_max+X_INT,X_INT): count[time] = 0

	for key in count:
		count[key] = len([time for time in t if time <= key])
	
	x_values = sorted(count)
	y_values = [count[x] for x in x_values]
	log_x = [log(s,10) for s in x_values]
	log_y = [log(s,10) for s in y_values]

	m1,b1 = np.polyfit(log_x[:GAP_START], log_y[:GAP_START],1)
	m2,b2 = np.polyfit(log_x[GAP_END:], log_y[GAP_END:], 1)
	m_ave = (m1+m2)/2
	b_ave = (b1+b2)/2

	print "m1: ",m1,"\tb1: ",b1
	print "m2: ",m2,"\tb2: ",b2
	print "m_ave: ", m_ave, "\tb_ave: ",b_ave

	line1_y = [ 10**(m1*s + b1) for s in log_x[:GAP_START] ]
	line1_x = [ 10**s for s in log_x[:GAP_START] ]

	line2_y = [ 10**(m2*s + b2) for s in log_x[GAP_END:] ]
	line2_x = [ 10**s for s in log_x[GAP_END:] ]

	line1_y_extrap = [ 10**(m1*s + b1) for s in log_x[GAP_START-1:] ]
	line1_x_extrap = [ 10**s for s in log_x[GAP_START-1:] ]

	line2_y_extrap = [ 10**(m2*s + b2) for s in log_x[:GAP_END+1] ]
	line2_x_extrap = [ 10**s for s in log_x[:GAP_END+1] ]

	line_ave_y = [ 10**(m_ave*s + b_ave) for s in log_x ]
	line_ave_x = [ 10**s for s in log_x ]

	line_lb_y = [ 10**(0.9*s + b_ave) for s in log_x ]
	line_ub_y = [ 10**(1.5*s + b_ave) for s in log_x ]
	line_bound_x = [ 10**s for s in log_x ]
	
	fig = plt.figure()
	ax = fig.add_subplot(111)

	ax.set_xscale("log")
	ax.set_yscale("log")

	ax.set_xlim( 0.8, max(x_values)+10 )
	ax.set_ylim( min(y_values)-50, max(y_values)+250 )

	ax.set_xlabel( "Days since main shock" )
	ax.set_ylabel( "Cumulative number of events" )

	ax.set_title( "Haida Gwaii Aftershock Sequence: Cumulative Event Count" )


	ax.plot(x_values,y_values,"o")

	ax.plot(line1_x,line1_y,"r")
	ax.plot(line1_x_extrap,line1_y_extrap,"r--")

	ax.plot(line2_x,line2_y,"r")
	ax.plot(line2_x_extrap,line2_y_extrap,"r--")

	ax.plot(line_ave_x,line_ave_y,"k")

	ax.plot(line_bound_x,line_lb_y,".")
	ax.plot(line_bound_x,line_ub_y,"*")
###
	fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.set_xlim( -1, max(x_values)+1 )
        ax.set_ylim( min(y_values)-50, max(y_values)+50 )

        ax.set_xlabel( "Days since main shock" )
        ax.set_ylabel( "Cumulative number of events" )

        ax.set_title( "Haida Gwaii Aftershock Sequence: Cumulative Event Count" )

        ax.plot(x_values,y_values,"o")

        ax.plot(line1_x,line1_y,"r")
        ax.plot(line1_x_extrap,line1_y_extrap,"r--")

        ax.plot(line2_x,line2_y,"r")
        ax.plot(line2_x_extrap,line2_y_extrap,"r--")

	ax.plot(line_ave_x,line_ave_y,"k")

	ax.plot(line_bound_x,line_lb_y,".")
	ax.plot(line_bound_x,line_ub_y,"*")
###	

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

#plot_omori(t,mag)

plot_omori_log_log(t,mag)

#ax2 = fig.add_subplot(212)
#ax2.plot(t,mag,"ko")
#ax2.set_xlabel( "Days since main shock" )
#ax2.set_ylabel( "Magnitude" )
plt.savefig(args.output_file[0])
plt.show()
