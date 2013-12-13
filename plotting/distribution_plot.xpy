def plot_distribution(tr, args):
    from numpy import arange, digitize
    import matplotlib.pyplot as plt
    bw = args.bin_width[0]
    if args.filter: tr.filter(args.filter[0])
    d = tr.data()
    mean = sum(d)/len(d)
    m = max([abs(val) for val in d])
    m = m - (m % bw) + 1.5*bw
    bins = arange(-m, m+bw, bw)
    inds = digitize(d, bins)
    counts = [len(filter(lambda ind: i+1 == ind, inds)) for i in 
        range(len(bins))]
    fig = plt.figure()
    fig.suptitle("%s:%s %s - %s" % (args.sta[0], args.chan[0], args.tstart[0],\
        args.tend[0]), fontsize=18)
    ax = fig.add_subplot(2, 1, 1)
    ax.plot(d)
    ax.set_xlabel("Sample Index")
    ax.set_ylabel("Counts")
    ax = fig.add_subplot(2, 1, 2)
    ax.bar(bins, counts, bw)
    ax.axvline(x=mean, color='k', linestyle='--')
    ax.set_xlabel("Counts")
    ax.set_ylabel("Count")
    if args.save_as: plt.savefig("%s.png" % args.save_as[0], format='png')
    plt.show()

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Plot distribution of "\
        "seismic trace amplitudes.")
    parser.add_argument('db', nargs=1, type=str, help="input database")
    parser.add_argument('sta', nargs=1, type=str, help="station")
    parser.add_argument('chan', nargs=1, type=str, help="channel")
    parser.add_argument('tstart', nargs=1, type=str, help="start time " \
        "- '2013324 00:00:00'")
    parser.add_argument('tend', nargs=1, type=str, help="end time " \
        "- '2013324 12:00:00'")
    parser.add_argument('bin_width', nargs=1, type=float, help="bin width")
    parser.add_argument('-f', '--filter', nargs=1, type=str, help="filter")
    parser.add_argument('-s', '--save_as', nargs=1, type=str,
        help="Save plot as.")
    args = parser.parse_args()
    if not os.path.isfile(args.db[0]):
        sys.exit("Descriptor file %s does not exist."
            % args.db[0])
    return args
    
def main():
    from antelope.datascope import dbopen
    args = parse_args()
    db = dbopen(args.db[0], 'r')
    db = db.lookup(table='wfdisc')
    tr = db.loadchan(args.tstart[0], args.tend[0], args.sta[0], args.chan[0])
    tr.record = 0
    plot_distribution(tr, args)

if __name__ == '__main__': sys.exit(main())
else: print sys.argv[0], "- Not a module to import!"
