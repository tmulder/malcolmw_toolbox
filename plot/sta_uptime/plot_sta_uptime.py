# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 15:21:25 2013

@author: malcolm
"""
import matplotlib.pyplot as plt
import time

title = "Aftershock Station Up-Time"
input_file = "/home/malwhite/dropbox/hg_station_times.txt"
output_file = "/home/malwhite/dropbox/junk.png"

start_time, end_time = None, None
start_time = time.mktime(time.strptime("2012 09 30", "%Y %m %d"))
end_time = time.mktime(time.strptime("2013 03 02", "%Y %m %d"))


def sub2colour(sub):
    s2c = {"as":"#FF9933", "asr":"#FF3300", "cn":"#444444", "obs":"#0099FF","po":"#CCCCCC"}
    return s2c[sub]
    
def readFile( path ):
    infile = open(path,"r")
    sta_data = {}
    
    for line in infile:
        l = line.split()
        sta,ton,toff,sub = l[1:5]
        
        ts,te = time.strptime(ton,"%Y%j"), time.strptime(toff+" 23:59:59","%Y%j %H:%M:%S")
        if ts > te:
            print sta, "ontime > offtime"
            exit()
        bars = start_time if start_time and time.mktime(ts) < start_time else time.mktime(ts)#epoch start time
        barlen = (end_time-bars) if end_time and time.mktime(te) > end_time else (time.mktime(te)-bars) #epoch stop time
        
        if not sta in sta_data: sta_data[sta] = [[(bars,barlen)],(sub2colour(sub),)]
        else:
            sta_data[sta][0].append((bars,barlen))
            temp=list(sta_data[sta][1])
            temp.append(sub2colour(sub))
            sta_data[sta][1] = tuple(temp)
    return sta_data

def plot(sta_data):
    stas_r = reversed(sorted(sta_data.keys()))
    stas = [ sta for sta in stas_r ]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bar_height = 9 #this is the thickness of the bar
    bar_dist = 10 #this is the distance between bar centers
    nsta=0
    
    for sta in stas:
        ax.broken_barh(sta_data[sta][0],((nsta*bar_dist+bar_dist/2), bar_height),facecolors=sta_data[sta][1])
        nsta+=1
        
    ax.set_ylim(0,nsta*bar_height)
    xmin, xmax = xminmax(sta_data)
    ax.set_xlim(xmin, xmax)
    xticks,xlabels = x_ticks_labels(xmin, xmax)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)
    ax.set_xlabel('2012/2013')

    ax.set_ylim(0,(nsta+1)*bar_dist)
    ax.set_yticks([j*bar_dist for j in range(1,nsta+1)])
    ax.set_yticklabels([sta for sta in stas])
    ax.set_ylabel('Station Code')
    ax.grid(True)
    
#    make_legend(ax)
    plt.title(title)
    plt.savefig(output_file)
    plt.show()

def make_legend(ax):
    p,q,r,s,t = Rectangle((0,0),1,1,fc=sub2colour("as")), Rectangle((0,0),1,1,fc=sub2colour("asr")), Rectangle((0,0),1,1,fc=sub2colour("obs")), Rectangle((0,0),1,1,fc=sub2colour("cn")), Rectangle((0,0),1,1,fc=sub2colour("po"))
    #ax.legend([p,q,r,s,t],["Aftershock","Aftershock RT","OBS","Permanent","Potential Recovery"],bbox_to_anchor=(0,0,1.1,1.1),fancybox=True,shadow=True, loc=7)#'upper right')    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.15, box.width, box.height * 0.9])
    ax.legend([p,q,r,s,t],["Aftershock","Aftershock RT","OBS","Permanent","Potential Recovery"],bbox_to_anchor=(0.,-0.275,1.,.102),fancybox=True,shadow=True, loc=8,ncol=3)
    
def xminmax(sta_data):
    xstart,xend = [],[]
    for sta in sta_data:
        for j in range(len(sta_data[sta][0])):
            xstart.append(sta_data[sta][0][j][0])
            xend.append(sta_data[sta][0][j][1] + sta_data[sta][0][j][0])
    xmin = start_time if start_time else min(xstart) - 864000 #less 10 days
    xmax = end_time if end_time else max(xend) + 864000 #plus 10 days
    return xmin, xmax    

def x_ticks_labels(xmin,xmax):
    months = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sept", 10:"Oct", 11:"Nov", 12:"Dec"}
    ts = time.strptime(time.ctime(xmin), "%a %b %d %H:%M:%S %Y")
    te = time.strptime(time.ctime(xmax), "%a %b %d %H:%M:%S %Y")
    labels,ticks = [],[]
    
    ts_year, ts_mon = ts.tm_year, ts.tm_mon
    te_year, te_mon = te.tm_year, te.tm_mon
    
    month = 1 if ts_mon == 12 else ts_mon+1
    year = ts_year+1 if month == 1 else ts_year

    while year < te_year or (year == te_year and month <= te_mon):
        labels.append("%s 01" % months[month])
        t_str = "%4d %02d 01 00:00:00" % (year,month)
        t = time.strptime(t_str,"%Y %m %d %H:%M:%S")
        ticks.append(time.mktime(t))
        
        month = 1 if month == 12 else month+1
        year = year+1 if month ==1 else year
        
    return ticks, labels
    
plot(readFile(input_file))
