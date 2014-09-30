import sys
import os
import time
sys.path.append('%s/data/python' % os.environ['ANTELOPE'])
from antelope.datascope import closing, dbopen
from antelope.stock import str2epoch

def _parse_args():
    """
    Parse command line arguments, return dictionary-like object of
    results.
    """
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('db', type=str, help='Input database.')
    parser.add_argument('-p',
                        '--parameter_file',
                        type=str,
                        help='Parameter file.')
    return parser.parse_args()

def _read_pf(parameter_file):
    """
    Read and return contents of parameter file.
    """
    from antelope.stock import pfread, pfin
    if parameter_file:
        if os.path.splitext(parameter_file)[1] == '.pf':
            paramter_file = pfin(parameter_file)
        else:
            parameter_file = pfin('%s.pf' % parameter_file)
    else:
        parameter_file = pfread('plot_gaps')
    parameter_file = parameter_file.pf2dict()
    parameter_file['plot_start_time'] = eval(parameter_file['plot_start_time'])
    parameter_file['plot_end_time'] = eval(parameter_file['plot_end_time'])
    return parameter_file

def _get_sta_list(args):
    """
    Return list of station of uptimes.
    """
    with closing(dbopen(args.db, 'r')) as db:
        tbl_site = db.schema_tables['site']
        subset_expression = 'sta =~ /%s/' % args.parameter_file['sta_match'][0]
        for sta in args.parameter_file['sta_match'][1:]:
            subset_expression =  '%s || sta =~ /%s/' % (subset_expression, sta)
        tbl_site = tbl_site.subset(subset_expression)
        tbl_site = tbl_site.sort('sta', unique=True)
        stas = []
        for record in tbl_site.iter_record():
            stas += [record.getv('sta')[0]]
        return stas

class Station:
    """
    A class to hold basic stations data and station uptimes.
    """
    def __init__(self, sta, args):
        """
        Standard constructor method.
        """
        self.sta = sta
        plot_start_time = args.parameter_file['plot_start_time']
        plot_end_time = args.parameter_file['plot_end_time']
        with closing(dbopen(args.db, 'r')) as db:
            tbl_gap = db.schema_tables['gap']
            tbl_gap = tbl_gap.subset('sta =~ /%s/' % sta)
            tbl_gap = tbl_gap.subset('time >= _%f_ && time < _%f_' % \
                    (plot_start_time, plot_end_time))
            #Only considering vertical channels right now
            tbl_gap = tbl_gap.subset('chan =~ /..Z/')
            tbl_gap = tbl_gap.sort('time')
            tbl_site = db.schema_tables['site']
            tbl_site = tbl_site.subset('sta =~ /%s/' % sta)
            if tbl_site.record_count > 1:
                print 'More than one row in the site table for station %s' % sta
                print 'This may effect the plot'
            tbl_site.record = 0
            ondate, offdate = tbl_site.getv('ondate', 'offdate')
            ondate =  str2epoch('%d' % ondate)
            offdate = str2epoch('%d' % offdate)
            self.uptimes = [(plot_start_time,
                            (plot_end_time - plot_start_time))]
            tstart = ondate if ondate > plot_start_time else plot_start_time
            if offdate == -1.0 or plot_end_time < offdate:
                tend = plot_end_time
                tlength = tend - tstart
            else:
                tend = offdate
                tlength = tend - tstart
            self.uptimes = [(tstart, tlength)]
            for record in tbl_gap.iter_record():
                #first update the ontime length of the last ontime entry
                tstart = self.uptimes[-1][0]
                gap_tstart, gap_tlength = record.getv('time', 'tgap')
                ontime_length = gap_tstart - tstart
                self.uptimes[-1] = (tstart, ontime_length)
                #then add a new ontime entry from the end of the gap to the end of the plot time
                tstart = gap_tstart + gap_tlength
                if tstart > tend: continue
                #tlength = plot_end_time - tstart
                #if tlength < 0 or tstart + tlength > plot_end_time:
                #    tlength
                self.uptimes += [(tstart, tend - tstart)]

def _plot(stas, args):
    """
    Generate plot.
    """
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    bar_height = 10
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1)
    j = 0
    yticks, yticklabels = [], []
    groups = args.parameter_file['groups']
    colours = args.parameter_file['colours']
    for sta in reversed(stas):
        colour = '#%s' % colours[groups[sta.sta]]
        ax.broken_barh(sta.uptimes,
                       (j * bar_height, bar_height),
                       facecolors=colour)
        yticks += [j * bar_height + bar_height / 2]
        yticklabels += [sta.sta]
        j += 1
    for group in colours:
        ax.bar(0, 0, color='#%s' % colours[group], label=group)
    ax.vlines([eval(args.parameter_file['study_start_time']),
              eval(args.parameter_file['study_end_time'])],
              0,
              len(stas) * bar_height,
              linestyles='dashed',
              linewidth=1.5)
    ax.vlines(eval(args.parameter_file['main_shock_time']),
              0,
              len(stas) * bar_height,
              linestyles='solid',
              linewidth=2.5)
    ax.annotate('Main shock',
                (args.parameter_file['main_shock_time'],
                    len(stas) * 0.5 * bar_height),
                xycoords='data',
                xytext=(0.35, 0.45),
                textcoords='axes fraction',
                fontproperties=FontProperties(size=14),
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='right')
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_ylim(0, len(stas) * bar_height)
    ax.set_ylabel(args.parameter_file['ylabel'], fontsize=14)
    xticks, xticklabels = _get_xticks_and_xticklabels(args)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels)
    ax.set_xlabel(args.parameter_file['xlabel'], fontsize=14)
    ax.set_xlim(args.parameter_file['plot_start_time'],
                args.parameter_file['plot_end_time'])
    ax.grid(True)
    _add_legend(ax, args)
    fig.suptitle(args.parameter_file['title'], fontsize=16)
    plt.show()

def _add_legend(ax, args):
    from matplotlib.patches import Rectangle
    colours = args.parameter_file['colours']
    groups, rectangles = [], []
    for group in colours:
        colour = '#%s' % colours[group]
        groups += [group]
        rectangles += [Rectangle((0, 0), 1, 1, fc=colour)]
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.10, box.width, box.height * 0.95])
    ax.legend(rectangles, groups,
              fancybox=True,
              ncol=3,
              loc='lower center',
              bbox_to_anchor=(0.5, -0.175))
              #bbox_to_anchor=(0, -0.25, 1, 1))


def _get_xticks_and_xticklabels(args):
    months = {1:"Jan",
              2:"Feb",
              3:"Mar",
              4:"Apr",
              5:"May",
              6:"Jun",
              7:"Jul",
              8:"Aug",
              9:"Sept",
              10:"Oct",
              11:"Nov",
              12:"Dec"}
    plot_start_time = args.parameter_file['plot_start_time']
    plot_end_time = args.parameter_file['plot_end_time']
    ts = time.strptime(time.ctime(plot_start_time), "%a %b %d %H:%M:%S %Y")
    te = time.strptime(time.ctime(plot_end_time), "%a %b %d %H:%M:%S %Y")
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

if __name__ == '__main__':
    """
    Begin execution control here.
    """
    args = _parse_args()
    args.parameter_file = _read_pf(args.parameter_file)
    sta_match = _get_sta_list(args)
    stas = []
    for sta in sta_match:
        stas += [Station(sta, args)]
    _plot(stas, args)

else:
    print 'Not a module to import!!'
