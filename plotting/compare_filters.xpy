def plot_filter_comparison(tr1, args):
    from numpy import arange, digitize
    import matplotlib.pyplot as plt
    d = tr1.data()
    tr2 = tr1.trcopy()
    tr1.filter(args.filter1[0])
    tr2.filter(args.filter2[0])
    d1 = tr1.data()
    d2 = tr2.data()
    fig = plt.figure()
    fig.suptitle("%s:%s %s - %s" % (args.sta[0], args.chan[0], args.tstart[0],\
        args.tend[0]), fontsize=18)
    ax = fig.add_subplot(3, 1, 1)
    ax.plot(d)
    ax.set_xlabel("Sample Index")
    ax.set_ylabel("Counts")
    ax = fig.add_subplot(3, 1, 2)
    ax.plot(d1)
    ax.set_xlabel("Sample Index")
    ax.set_ylabel("Counts")
    ax.text(0.05*len(d1), 0.9*max(d1), args.filter1[0])
    ax = fig.add_subplot(3, 1, 3)
    ax.plot(d2)
    ax.set_xlabel("Sample Index")
    ax.set_ylabel("Counts")
    ax.text(0.05*len(d2), 0.9*max(d2), args.filter2[0])
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
    parser.add_argument('filter1', nargs=1, type=str, help="filter 1")
    parser.add_argument('filter2', nargs=1, type=str, help="filter 2")
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
    plot_filter_comparison(tr, args)

if __name__ == '__main__': sys.exit(main())
else: print sys.argv[0], "- Not a module to import!"
