from argparse import ArgumentParser
from obspy.core import read
from obspy.signal import highpass
parser = ArgumentParser()
parser.add_argument('output', type=str, help='output file')
parser.add_argument('scale', type=float, help='scale')
args = parser.parse_args()
scale = args.scale
stream = read('/Users/mcwhite/staging/dbs/anza_sub/2013/WWC/i4.WWC.BHZ.2013271_0+')
stream[0].data = highpass(stream[0].data, 2.0, corners=1, zerophase=True, df=stream[0].stats.sampling_rate)
stream.plot(type='dayplot', outfile=args.output, vertical_scaling_range=scale)

