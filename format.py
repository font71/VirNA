#!/usr/bin/env python3

from Bio import AlignIO
import sys
import getopt


def usage():
    print("Usage:")
    print(" -i, --input FILE")
    print("     The multiple alignment file")
    print(" -o, --output FILE")
    print("     The output file in json format")
    print(" -f, --inputformat [clustal | maf | nexus | stockholm | phylip-relaxed]")
    print("     The format of input file")
    print(" -h, --help")
    print("     Print this help")

filein = None
fformat = None
fileout = None

try:
    opts, args = getopt.getopt(sys.argv[1:], "i:f:o:h", [
                                   "input=", "inputformat=", "output=", "help"])
except getopt.GetoptError:
        usage()
        sys.exit(1)

for opt, arg in opts:
    if opt in ('-i', '--input'):
        filein = arg
    elif opt in ('-f', '--inputformat'):
        fformat = arg
    elif opt in ('-o', '--output'):
        fileout = arg
    elif opt in ('-h', '--help'):
        usage()
        sys.exit()
    else:
        usage()
        sys.exit(1)

if filein is None or fformat is None:
    usage()
    sys.exit(1)

align = AlignIO.read(filein, fformat)
oh = open(fileout, 'w')
AlignIO.write(align, oh, 'fasta')