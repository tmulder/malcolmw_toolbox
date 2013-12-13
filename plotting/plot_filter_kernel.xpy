def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Plot the kernel of the input"\
            " filter.")
    parser.add_argument('filt', nargs=1, type=str, help="filter")
    parser.add_argument('twin', nargs=1, type=float, help="time window")
    return parser.parse_args()

def plot_kernel(filt, twin):
    from antelope.datascope import dbcreate, dbopen
    import matplotlib.pyplot as plt
    SAMPRATE = 100.0
    dbcreate("/tmp/tmpdb_plot_filter_kernel", "Trace4.1")
    tr = dbopen("/tmp/tmpdb_plot_filter_kernel", 'r')
    tr = tr.lookup(table="trace")
    tr.record = tr.addnull()
    tr.putdata([0.0 if i > 0 else 1.0 for i in range(int(twin*SAMPRATE))])
    tr.putv("samprate", SAMPRATE)
    tr.filter(filt)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(tr.data())
    plt.show()

def main():
    args = parse_args()
    plot_kernel(args.filt[0], args.twin[0])

if __name__ == '__main__': sys.exit(main())
else: sys.exit("Not a module to import!!")
