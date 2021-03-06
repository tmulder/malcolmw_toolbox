from antelope.datascope import closing, dbopen
from obspy.core import read, Stream, Trace

def _get_traces(db, sta1, chan1, ts1, te1, sta2, chan2, ts2, te2):
    streams = []
    with closing(dbopen(db, 'r')) as db:
        for sta, chan, ts, te in [(sta1, chan1, ts1, te1),
                                  (sta2, chan2, ts2, te2)]:
            tbl_wfdisc = db.schema_tables['wfdisc']
            #read sta1:chan1
            tbl_wfdisc = tbl_wfdisc.subset('sta =~ /%s/ && chan =~ /%s/ && '
                                        'endtime >= _%s_ && time <= _%s_'
                                        % (sta, chan, ts, te))
            st = Stream()
            for record in tbl_wfdisc.iter_record():
                st += read(record.extfile()[1])
            streams += [st]
    return streams

def _plot_correlation(a, b):
    import matplotlib.pyplot as plt
    from scipy.signal import correlate
    d = correlate(a, b, "full")
    fig = plt.figure()
    ax = fig.add_subplot(3, 1, 1)
    ax.plot(d)
    ax = fig.add_subplot(3, 1, 2)
    ax.plot(a)
    ax = fig.add_subplot(3, 1, 3)
    ax.plot(b)
    plt.show()

def _preprocess(streams):
    #demean and detrend data
    for i in range(2):
        #streams[i].detrend('linear')
        streams[i].detrend('demean')
    for i in range(2):
        print len(streams[i])
        streams[i].merge(fill_value=0)
        print len(streams[i])
    return streams

def _parse_args():
    import argparse
    import scipy
    parser = argparse.ArgumentParser(description="Plot cross-correlation two"\
            " traces.")
    parser.add_argument('db', type=str, help="dbin")
    parser.add_argument('sta1', type=str,  help="station 1")
    parser.add_argument('chan1', type=str, help="channel 1")
    parser.add_argument('time1', type=str, help="start time 1")
    parser.add_argument('endtime1', type=str, help="end time 1")
    parser.add_argument('sta2', type=str, help="station 2")
    parser.add_argument('chan2', type=str, help="channel 2")
    parser.add_argument('time2', type=str, help="start time 2")
    parser.add_argument('endtime2', type=str, help="end time 2")
    return parser.parse_args()

def main():
    args = _parse_args()
    streams = _get_traces(args.db, args.sta1, args.chan1, args.time1,
                          args.endtime1, args.sta2, args.chan2, args.time2,
                          args.endtime2)
    streams = _preprocess(streams)
    streams[0].plot()
    #_plot_correlation(a, b)

if __name__ == '__main__': sys.exit(main())
else: sys.exit("Not a moduel to import!!")
