from antelope.datascope import closing, dbopen
def _parse_args():
    """
    Parse command line options.
    """
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('dbin', type=str, help='Input database.')
    parser.add_argument('-s', '--save_as', type=str,
            help='Save output to file.')
    parser.add_argument('-p', '--parameter_file', type=str,
            help='Parameter file.')
    parser.add_argument('-i', '--interval', type=float,
            help='x interval (sample spacing) in number of days.')
    parser.add_argument('-g', '--gaps', nargs='+', type=float,
            help='Specify gaps over which to ignore data when curve fitting.'\
                'Specify as GAP_START [GAP_END [GAP_START...]] in decimal '\
                'days.')
    parser.add_argument('-f', '--fit_curve', action='store_true',
            help='Bin width.')
    parser.add_argument('-l', '--log_log_scale', action='store_true',
            help='Scale axes logarithmically.')
    return parser.parse_args()

def _read_pf(args):
    """
    Read and return contents of parameter file.
    """
    from antelope.stock import pfread, pfin
    parameter_file = args.parameter_file
    if parameter_file:
        if os.path.splitext(parameter_file)[1] == '.pf':
            paramter_file = pfin(parameter_file)
        else:
            parameter_file = pfin('%s.pf' % parameter_file)
    else:
        parameter_file = pfread('plot_omori')
    args.parameter_file = parameter_file.pf2dict()
    return args

def _read_data(args):
    """
    Read and return data from database.
    """
    with closing(dbopen(args.dbin, 'r')) as db:
        view = db.schema_tables['origin']
        view = view.join('event')
        view = view.subset('orid == prefor')
        view = view.join('netmag')
        args.times = [record.getv('time')[0] / 86400.0\
                for record in view.iter_record()]
        min_time = min(args.times)
        args.times = [t - min_time + 1 for t in args.times]
    return args

def _plot(args):
    """
    Make a cool plot.
    """
    from numpy import arange, digitize, zeros
    import matplotlib.pyplot as plt
    parameter_file = args.parameter_file
    interval = args.x_int if args.interval else 1.0
    t_max = max(args.times)
    bins = arange(0, t_max + interval, interval)
    count = zeros(len(bins))
    inds = digitize(args.times, bins)
    for i in inds:
        count[i - 1] += 1
    total = count.cumsum()
    x_values = [b for b in bins]
    y_values = [t for t in total]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(parameter_file['title'])
    ax.set_xlabel(parameter_file['xlabel'])
    ax.set_ylabel(parameter_file['ylabel'])
    ax.plot(x_values, y_values, 'o', color='0.5')
    if args.fit_curve:
        A, m = _fit_data(x_values, y_values, args.gaps)
        curve_x = x_values
        curve_y = [A * pow(x, m) for x in x_values]
        ax.plot(curve_x, curve_y, 'k', linestyle='--')
        bbox_props = dict(boxstyle='round', facecolor='0.05', alpha=0.25)
        ax.text(0.05, 0.95,
                '$N(t) = At^{(1-p)}$\n$A = %.3f$\n$p = %.3f$' % (A, abs(m - 1)),
                transform=ax.transAxes,
                fontsize=16,
                verticalalignment='top',
                bbox=bbox_props)
    if args.log_log_scale:
        ax.set_xscale('log')
        ax.set_yscale('log')
    if args.save_as:
        plt.savefig('%s.png' % args.save_as)
    plt.show()

def _fit_data(x_values, y_values, gaps):
    """
    Find and return parameters of best fitting line
    (least-squares sense) of log(x_values), log(y_values).

    Omori's law is: N(t) = A * t^(1 - p)
    """
    from math import log
    from numpy import polyfit
    #If there is a gap specified with -g option and no end specified,
    #assume the gap goes to the end of the dataset.
    if gaps != None and len(gaps) % 2 != 0:
        gaps.append(x_values[-1])
    #Remove data falling within gap
    while gaps != None and len(gaps) != 0:
        gap_start, gap_end = gaps.pop(0), gaps.pop(0)
        y_values = [y_values[i] for i in range(len(x_values))
                if not (x_values[i] >= gap_start and x_values[i] <= gap_end)]
        x_values = [x_values[i] for i in range(len(x_values))
                if not (x_values[i] >= gap_start and x_values[i] <= gap_end)]
    log_x = [log(x, 10) if x != 0 else 0 for x in x_values]
    log_y = [log(y, 10) if y != 0 else 0 for y in y_values]
    slope, intercept = polyfit(log_x, log_y, 1)
    #Calculate A from Omori's law
    A = pow(10, intercept)
    #Return A, (1- p)
    return A, slope


if __name__ == '__main__':
    _plot(_read_data(_read_pf(_parse_args())))
else:
    print 'plot_omori - Not a module to import!!'
