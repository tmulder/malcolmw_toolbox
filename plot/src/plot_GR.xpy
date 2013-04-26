import matplotlib.pyplot as plt
import numpy as np

import argparse
import sys.path
import os.environ

from math import log

sys.path.append(os.environ['ANTELOPE'] + '/data/python')

from antelope.datascope import *

def read_data(path):
	dbin = dbopen(path,"r")

	dbin = dbin.lookup(table="origin")
	dbin = dbin.join("event")
	dbin = dbin.subset("orid==prefor")
	dbin = dbin.join("netmag")

	nrec = dbin.nrecs()

	mag = [ dbin.getv("magnitude") for dbin[3] in range(nrec) ]
	time = [ dbin.getv("time")[0]/(24*60*60) for dbin[3] in range(nrec) ]

	time = [ time[i] if not mag[i] == -999.00 for i in range(len(time)) ]
	mag = [ m if not m == -999.00 for m in mag ]

	min_time = min(time)
	time = [ t - min_time for t in time ]

	return time,mag
	

def readfile(path):
	"""Read data from input file."""
        infile = open( path, "r" )

        magnitude, t = [],[]

        for line in infile:
                l = line.split()
                magnitude.append(float(l[0]))
                t.append(float(l[1]))
        return t, magnitude

def plot_gutenberg_richter(mag,log_y_scale):
	"""Generate plot showing Gutenberg-Richter relationship."""
        #IMPROVEMENT
        #maximum likelihood estimator should be used to determine a,b as opposed to least squares method
        #see http://pasadena.wr.usgs.gov/office/kfelzer/AGU2006Talk.pdf

	print "\nCAVEAT"
	print "Maximum likelihood estimator should be used to estimate a and b values."
	print "Least squares method currently implemented for convenience."
	print "see http://pasadena.wr.usgs.gov/office/kfelzer/AGU2006Talk.pdf"

        X_INT = 0.1
        COMPLETENESS_LB = 2.5
        COMPLETENESS_UB = 6.0
        EXTRAP_LB = 1.0
        EXTRAP_UB = 9.0

        count = {}
        for i in np.arange(-1.0,10.0, X_INT):
                count[i] = 0

        for m in mag:
                for key in count:
                        if m >= key: count[key] += 1

        N=len(mag)

        x_values = sorted(count)
        y_values = [ count[x] for x in x_values ]

	y_max = max(y_values)

        x_to_fit, y_to_fit = [],[]
        for x_val in x_values:
                if x_val > COMPLETENESS_LB and x_val <= COMPLETENESS_UB:
                        x_to_fit.append(x_val)
                        y_to_fit.append(log(count[x_val],10)) if not count[x_val] == 0 else y_to_fit.append(0)

        b,a = np.polyfit(x_to_fit, y_to_fit, 1)
        b=abs(b)

        def gr_reln(m):
                return 10**(a-b*m)

        line_x_values = np.arange(COMPLETENESS_LB,COMPLETENESS_UB,X_INT)
        line_y_values = [gr_reln(x) for x in line_x_values]
        #extrap_x_values = [x for x in list(np.arange(EXTRAP_LB, COMPLETENESS_LB, X_INT))+list(np.arange(COMPLETENESS_UB, EXTRAP_UB, X_INT))]
        extrap_x_values = [x for x in list(np.arange(EXTRAP_LB, EXTRAP_UB, X_INT)) if x not in line_x_values]
        extrap_y_values = [gr_reln(x) for x in extrap_x_values]

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title( "Haida Gwaii Aftershock Sequence: Gutenberg-Richter Relationship" )

        ax.plot( x_values, y_values, "bo" )
        ax.plot( line_x_values, line_y_values, "r" )
        ax.plot( extrap_x_values, extrap_y_values, "r--" )

        ax.set_xlabel( "Magnitude, M" )
        ax.set_ylabel( "# of Events >= M, N(M)" )


        if log_y_scale:
		ax.set_yscale("log")

        	ax.set_xlim( -1.2, 9.0 )
        	ax.set_ylim( 0.5, y_max+0.3*y_max)

       		ax.text( 6.0, 0.1*y_max, "a=%.3f, b=%.3f" % (a,b) )

	else:
		ax.set_xlim(-1.2,9.0)
		ax.set_ylim(0,y_max+0.05*y_max)

       		ax.text( 6.0, 0.9*y_max, "a=%.3f, b=%.3f" % (a,b) )

parser = argparse.ArgumentParser(description="Plot Gutenberg-Richter relationship.")
parser.add_argument('input_file',metavar='infile',type=str,nargs=1,\
                help = "Input file")
parser.add_argument('-l','--log_y_scale',action='store_true',help='scale y axis logarithmically')
parser.add_argument('-s',dest='output_file',nargs=1,help='save output to specified file' )

args = parser.parse_args()

t,mag = readfile(args.input_file[0])

plot_gutenberg_richter(mag,args.log_y_scale)

if args.output_file: plt.savefig(args.output_file[0] + '.png')

plt.show()
