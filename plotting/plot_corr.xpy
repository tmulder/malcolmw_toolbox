def _get_trace(db, sta, chan, time, endtime):
    from antelope.datascope import dbopen
    db = dbopen(db, 'r')
    db = db.lookup(table='wfdisc')
    tr = db.loadchan(time, endtime, sta, chan)
    db.close()
    tr.record = 0
    return tr

def _plot_correlation(a, b):
    import matplotlib.pyplot as plt
    from numpy import correlate
    d = correlate(a, b)
    fig = plt.figure()
    ax = fig.add_subplot(3, 1, 1)
    ax.plot(d)
    ax = fig.add_subplot(3, 1, 2)
    ax.plot(a)
    ax = fig.add_subplot(3, 1, 3)
    ax.plot(b)
    plt.show()

def _parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Plot cross-correlation two"\
            " traces.")
    parser.add_argument('db', nargs=1, type=str, help="dbin")
    parser.add_argument('sta1', nargs=1, type=str,  help="station 1")
    parser.add_argument('chan1', nargs=1, type=str, help="channel 1")
    parser.add_argument('time1', nargs=1, type=str, help="start time 1")
    parser.add_argument('endtime1', nargs=1, type=str, help="end time 1")
    parser.add_argument('sta2', nargs=1, type=str, help="station 2")
    parser.add_argument('chan2', nargs=1, type=str, help="channel 2")
    parser.add_argument('time2', nargs=1, type=str, help="start time 2")
    parser.add_argument('endtime2', nargs=1, type=str, help="end time 2")
    return parser.parse_args()

def main():
    args = _parse_args()
    a = _get_trace(args.db[0], args.sta1[0], args.chan1[0], args.time1[0], \
            args.endtime1[0])
    b = _get_trace(args.db[0], args.sta2[0], args.chan2[0], args.time2[0], \
            args.endtime2[0])
    _plot_correlation(a.data(), b.data())

if __name__ == '__main__': sys.exit(main())
else: sys.exit("Not a moduel to import!!")
