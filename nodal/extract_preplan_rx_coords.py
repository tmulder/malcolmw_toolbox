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
    for dir in args.segd_dirs:
        string =  "Processing %s" % dir
        print string
        print "=" * len(string)
        for file in sorted(os.listdir(dir)):
            print "\tProcessing %s" % file
            segd = SegD('%s/%s' % (dir, file))
            x, y = segd.get_rx_coords_preplan()
            lat, lon = utm2latlon(x, y, 11, 'S')
            outfile.write('%s %s %.6f %.6f\n' % (file[:3], file[4:6], lon, lat))
    outfile.close()

