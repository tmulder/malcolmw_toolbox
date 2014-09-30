def _parse_args():
    """
    Parse command line options.
    """
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('dbin', type=str, help='Input database.')
    parser.add_argument('m_cutoff', type=float,
            help='Threshold (cut-off) magnitude.')
    parser.add_argument('-s', '--save_as', type=str,
            help='Save output to file.')
    parser.add_argument('-b', '--bin_width', type=float,
            help='Bin width.')
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
        parameter_file = pfread('plot_gr')
    args.parameter_file = parameter_file.pf2dict()
    args.parameter_file['x_axis_lower_limit'] = \
            eval(args.parameter_file['x_axis_lower_limit'])
    return args

def _read_data(args):
    """
    Read and return data from database.
    """
    if not os.path.isfile(args.dbin):
        print "Input database does not exist. Please check path."
        sys.exit(-1)
    with closing(dbopen(args.dbin, 'r')) as db:
        view = db.schema_tables['origin']
        view = view.join('event')
        view = view.subset('orid == prefor')
        view = view.join('netmag')
        args.mags = filter(lambda v: v != -999.00,
                [record.getv('magnitude')[0] for record in view.iter_record()])
    return args

def _plot(args):
    """
    Make a cool plot.
    """
    from numpy import arange, digitize, zeros, mean
    from math import log, e, sqrt
    import matplotlib.pyplot as plt
    parameter_file = args.parameter_file
    bin_width = args.bin_width if args.bin_width else 0.1
    #m_cutoff = args.m_cutoff - bin_width / 2.0
    m_cutoff = args.m_cutoff
    mags_filtered = filter(lambda v: v >= m_cutoff, args.mags)
    #Create an array of bin boundaries
    bins = arange(-1.0, 9.0, bin_width)
    #Get array of indices mapping magnitudes to bins
    inds = digitize(args.mags, bins)
    #inds_filtered = digitize(mags_filtered, bins)
    #Find the left-hand edge of each bin for plotting
    x_values = [a_bin - bin_width / 2.0 for a_bin in bins]
    y_values = zeros(len(x_values))
    for ind in inds: y_values[:ind] += 1
    y_values = list(y_values)
    #Calculate b-value using Maximum Likelihood Estimator
    mags_filtered_mean = mean(mags_filtered)
    b_prime = pow((mags_filtered_mean - m_cutoff), -1)
    b_value = b_prime * log(e, 10)
    kappa = len(mags_filtered)
    #Calculate the expected value for cumulative frequency at various magnitudes
    ex_values = [kappa * pow(e, (-b_prime * (m - m_cutoff))) for m in x_values]
    print '\nb = b\' * log(e)\n'
    #Calculate 95% confidence interval for b'
    conf_lb_b_prime = (1 - 1.96 / sqrt(kappa)) / (mean(mags_filtered) - m_cutoff)
    conf_ub_b_prime = (1 + 1.96 / sqrt(kappa)) / (mean(mags_filtered) - m_cutoff)
    #print 'b\' = %.4f\n95\% confidence interval: %.4f <= b\' <= %.4f' % \
    #        (b_prime, conf_lb_b_prime, conf_ub_b_prime)
    print "b' = %.4f" % b_prime, "\n95% confidence interval:", \
        "%.4f <= b' <= %.4f" % (conf_lb_b_prime, conf_ub_b_prime)
    #Calculate 95% confidence interval for b
    conf_lb_b = conf_lb_b_prime * log(e, 10)
    conf_ub_b = conf_ub_b_prime * log(e, 10)
    b_error = max([abs(b_value - a) for a in (conf_lb_b, conf_ub_b)])
    print "b = %.4f" % b_value, "\n95% confidence interval:", \
            "%.4f <= b <= %.4f" % (conf_lb_b, conf_ub_b)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(parameter_file['title'])
    ax.bar(x_values, y_values, width=bin_width, color='0.5')
    ax.plot(x_values, ex_values, 'k', linestyle='--')
    ax.set_xlabel(parameter_file['xlabel'])
    ax.set_ylabel(parameter_file['ylabel'])
    ax.set_xlim(parameter_file['x_axis_lower_limit'],
                x_values[y_values.index(0) + 1])
    ax.set_ylim(0, max(y_values) + 100)
    #Add a cool box with some info
    bbox_props = dict(boxstyle='round', facecolor='0.05', alpha=0.25)
    ax.text(0.70, 0.90,
            '$b = %.3f \pm %.3f$\n$M_{complete} = %.2f$' % (b_value, b_error, m_cutoff),
            transform=ax.transAxes,
            fontsize=16,
            verticalalignment='top',
            bbox=bbox_props)
    if args.save_as: plt.savefig('%s.png' % args.save_as)
    plt.show()

if __name__ == '__main__':
    from antelope.datascope import closing, dbopen
    _plot(_read_data(_read_pf(_parse_args())))
else:
    print 'plot_gr - Not a module to import!!'
