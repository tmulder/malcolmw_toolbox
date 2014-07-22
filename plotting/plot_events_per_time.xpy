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
    parser.add_argument('-b', '--bin_width', type=float,
            help='Bin width in days.')
    parser.add_argument('-o', '--omori_params', type=float, nargs=2,
            help='Omori decay curve parameters (A, p).')
    parser.add_argument('-p', '--parameter_file', type=str,
            help='Parameter file.')
    parser.add_argument('-l', '--log_y_scale', action='store_true',
            help='Scale y-axis logarithmically.')
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
        parameter_file = pfread('plot_events_per_time')
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
        args.times = [t - min_time for t in args.times]
    return args

def _plot(args):
    """
    Make a cool plot.
    """
    from numpy import arange, digitize, zeros
    import matplotlib.pyplot as plt
    parameter_file = args.parameter_file
    bin_width = args.bin_width if args.bin_width else 1.0
    t_max = max(args.times)
    bins = arange(0, t_max + bin_width, bin_width)
    inds = digitize(args.times, bins)
    x_values = [a_bin - (bin_width / 2.0) for a_bin in bins]
    y_values = zeros(len(x_values))
    for ind in inds: y_values[ind - 1] += 1
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    is_log = True if args.log_y_scale else False
    ax.bar(x_values, y_values, width=bin_width, log=is_log, color='0.5')
    if is_log:
        ax.set_yscale('log')
    if args.omori_params:
        A, p = args.omori_params[0], args.omori_params[1]
        curve_x = filter(lambda v: v != 0,
                         [x + (bin_width / 2.0) for x in x_values])
        curve_y = [A * (1 - p) * pow(x, -p) for x in curve_x]
        ax.plot(curve_x, curve_y, 'ko', linestyle='--')
    ax.set_title(parameter_file['title'])
    ax.set_xlabel(parameter_file['xlabel'])
    ax.set_ylabel(parameter_file['ylabel'])
    ax.set_xlim(x_values[0], x_values[-1] + bin_width)
    if args.save_as:
        plt.savefig('%s.png' % args.save_as)
    plt.show()


if __name__ == '__main__':
    _plot(_read_data(_read_pf(_parse_args())))
else:
    print 'plot_events_per_time - Not a module to import!!'
