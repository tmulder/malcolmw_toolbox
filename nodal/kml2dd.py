import sys
import re

def _parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("input", type=str, help="Input KML file.")
    parser.add_argument("output", type=str, help="Output LL file.")
    return parser.parse_args()

if __name__ == "__main__":
    args = _parse_args()
    infile = open(args.input, 'r')
    outfile = open(args.output, 'w')
    re_line_match = re.compile("<name>Line [1-9][0-9]?</name>")
    re_line_no = re.compile("[1-9][0-9]?")
    re_station_match = re.compile("<name>Station [1-9][0-9]?</name>")
    re_station_no = re.compile("[1-9][0-9]?")
    re_coord_start_match = re.compile("<coordinates>")
    re_coord_end_match = re.compile("</coordinates>")
    while True:
        line = infile.readline()
        if not line:
            break
        if re_line_match.search(line):
            match = re_line_no.search(line)
            line_no = int(line[match.start(): match.end()])
            string = "Processing line: %d" % line_no
            print string, "\n", "=" * len(string)
        elif re_station_match.search(line):
            match = re_station_no.search(line)
            col_no = int(line[match.start(): match.end()])
            sta = "R%02d %02d" % (line_no, col_no)
            print "\tProcesing station: %d" % col_no
        elif re_coord_start_match.search(line):
            lon_sum, lat_sum, n = 0, 0, 0
            line = infile.readline()
            while not re_coord_end_match.search(line):
                line = line.strip().split(",")
                lon_sum += float(line[0])
                lat_sum += float(line[1])
                n += 1
                line = infile.readline()
            lon = lon_sum / n
            lat = lat_sum / n
            outfile.write("%s %.6f %.6f\n" % (sta, lon, lat))
    infile.close()
    outfile.close()
    sys.exit(0)
