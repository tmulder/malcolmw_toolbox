def gaussian(x, sigma):
    from math import e, pi
    #return pow(e, -pow(x, 2)/(2.0*pow(sigma, 2)))
    return (1.0/(pow(2.0*pi, 0.5)*sigma))*pow(e, -pow(x, 2)/(2.0*pow(sigma, 2)))

def dgaussian(x, sigma):
    from math import e, pi
    return -(1.0/(pow(2.0*pi, 0.5)*sigma))*(x/pow(sigma, 2))*pow(e, -pow(x, 2)/(2.0*pow(sigma, 2)))

import sys
import os
sys.path.append("%s/data/python" % os.environ['ANTELOPE'])
from antelope.datascope import dbopen
import matplotlib.pyplot as plt
from numpy import linspace, convolve, zeros
db = dbopen("/anf/ANZA/rt/anza/anza", 'r')
db = db.lookup(table='wfdisc')
#ts = "2013270 00:00:00"
#te = "2013270 00:20:00"
#sta= 'PFO'
#chan = 'HNE'
#filename = '/Users/mcwhite/Desktop/figures/AutoQC/deriv_gaussian_step'
ts = "2013144 03:38:00"
te = "2013144 04:08:00"
sta = "B086A"
chan = "HHE"
filename = '/Users/mcwhite/Desktop/figures/AutoQC/deriv_gaussian_regional'
filename = '/Users/mcwhite/Desktop/figures/AutoQC/deriv_gaussian_kernel'
tr = db.loadchan(ts, te, sta, chan)
tr.record = 0
d = tr.data()
samprate, nsamp = tr.getv('samprate', 'nsamp')
tr.trdestroy()
dt = 1.0/samprate
sigma = 5*dt
if len(d) % 2 == 0: d = d[:-1]
dtimes = [i*dt for i in range(len(d))]
ftimes = linspace(-dtimes[len(dtimes)/2], dtimes[len(dtimes)/2], len(dtimes))
#f = [gaussian(i, 0.02) for i in arange(-1, 1, 0.01)]
f = [dgaussian(t, sigma) for t in ftimes] 
fig = plt.figure()
fig.suptitle('Gaussian derivative filter kernel', fontsize=16)
#fig.suptitle('%s:%s %s-%s' % (sta, chan, ts, te), fontsize=16)
#ax = fig.add_subplot(3, 1, 1)
#ax.plot(dtimes, d)
#ax = fig.add_subplot(3, 1, 2)
#ax.plot(ftimes, f)
#ax = fig.add_subplot(3, 1, 3)
nsmps = 5*int(sigma*samprate)
#c = convolve(d, f, mode='same')[nsmps:-nsmps]
#dtimes = dtimes[nsmps:-nsmps]
#ax.plot(dtimes, c)
ax = fig.add_subplot(1, 1, 1)
ax.plot(f[(len(f)/2)-5*nsmps : (len(f)/2)+5*nsmps])
plt.savefig('%s.png' % filename, format='png')
plt.show()

