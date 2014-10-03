"""
Extract pre-planned receiver coordinates from Seg-D files and output to a file.
"""
import sys
import os
from segd2db import SegD
from utm import to_latlon as utm2latlon

def _parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("outfile", type=str, help="Output file.")
    parser.add_argument("segd_dirs", type=str, nargs="+", help="SEGD data "
        "directory/directories")
    return parser.parse_args()

if __name__ == "__main__":
    args = _parse_args()
    outfile = open(args.outfile, 'w')
    stas = []
    for dir in args.segd_dirs:
        string =  "Processing %s" % dir
        print string
        print "=" * len(string)
        for file in sorted(os.listdir(dir)):
            sta = "%s %s" % (file[:3], file[4:6])
            if sta not in stas:
                stas += [sta]
                print "\tProcessing %s" % file
                segd = SegD('%s/%s' % (dir, file))
                x, y = segd.get_rx_coords_preplan()
                lat, lon = utm2latlon(x, y, 11, 'S')
                outfile.write('%s %.6f %.6f\n' % (sta, lon, lat))
    outfile.close()

