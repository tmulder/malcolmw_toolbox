import sys
import matplotlib.pyplot as plt

def _parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("input", type=str, help="Input coordinate file.")
    return parser.parse_args()

if __name__ == "__main__":
    args = _parse_args()
    infile = open(args.input, "r")
    plt.figure()
    for line in infile:
        line = line.split()
        prepl_lon, prepl_lat = float(line[2]), float(line[3])
        fin_lon, fin_lat = float(line[4]), float(line[5])
        dlon = fin_lon - prepl_lon
        dlat = fin_lat - prepl_lat
        plt.plot(prepl_lon, prepl_lat, 'bo')
        plt.plot(fin_lon, fin_lat, 'ro')
        #plt.arrow(prepl_lon, prepl_lat, dlon, dlat,
                #head_width=0.05,
                #head_length=0.1)
    plt.show()
    sys.exit(0)
