import sys

def _parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("preplan_input", type=str, help="Pre-plan rx "\
            "coordinate file.")
    parser.add_argument("final_input", type=str, help="Final rx coordinate "\
            "file.")
    parser.add_argument("output", type=str, help="Output file.")
    return parser.parse_args()

if __name__ == "__main__":
    args = _parse_args()
    prepl_infile = open(args.preplan_input, "r")
    fin_infile = open(args.final_input, "r")
    outfile = open(args.output, "w")
#Check to make sure station set in final coordinate file is contained
#by pre-planned file.
    for fin_line in fin_infile:
        sta = fin_line[:6]
        fin_line = fin_line.split()
        prepl_infile.seek(0)
        found_sta = False
        for prepl_line in prepl_infile:
            if prepl_line[:6] == sta:
                found_sta = True
                break
        if not found_sta:
            print "%s exists in final coordinate file but not in pre-plan "\
                    "coordinate file."
            sys.exit(-1)
#Check to make sure files contain the same number of lines
#    fin_infile.seek(0)
#    prepl_infile.seek(0)
#    fin_counter = 0
#    for line in fin_infile:
#        fin_counter += 1
#    prepl_counter = 0
#    for line in prepl_infile:
#        prepl_counter += 1
#    if fin_counter != prepl_counter:
#        print "Final coordinate file has %d lines and pre-plan coordinate "\
#                "file has %d lines" % (fin_counter, prepl_counter)
#        sys.exit(-1)
#Build the file like
#Line Column PrePlanLon PrePlanLat FinalLon FinalLat
    fin_infile.seek(0)
    prepl_infile.seek(0)
    for prepl_line in prepl_infile:
        sta = prepl_line[:6]
        print "Processing %s" % sta
        prepl_line = prepl_line.split()
        prepl_lon, prepl_lat = prepl_line[2], prepl_line[3]
        fin_infile.seek(0)
        for fin_line in fin_infile:
            if fin_line[:6] == sta:
                fin_line = fin_line.split()
                fin_lon, fin_lat = fin_line[2], fin_line[3]
                outfile.write("%s %s %s %s %s\n" % (sta,
                                                    prepl_lon,
                                                    prepl_lat,
                                                    fin_lon,
                                                    fin_lat))
                break
    prepl_infile.close()
    fin_infile.close()
    outfile.close()
    sys.exit(0)
