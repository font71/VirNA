#!/usr/bin/env python3

from libmat import libdist
from libmat.distance_matrix import Matrix
from libmat.msn2 import MinimumSpanningNetwork
from libmat.gml import GMLParser
import sys
import pandas as pd
import getopt
import os


def usage():
   print(" -m, --msa FILE")
   print("     The multiple alignment file in fasta format (Mandatory)")
   print(" -o, --outdir DIR")
   print("     Output directory (default: .)")
   print(" -p, --prefix STR")
   print("     The string to attach to every output files (default: \"\")")
   print(" -x, --matrix")
   print("     Dumps edit distance matrix")
   print(" -t, --borderth INT")
   print("     The multiple alignment will be trimmed at both ends using this value(default value 90)")
   print(" -i, --maxiter INT")
   print("     Maximum number of iterations to perform during MSN building")
   print(" -l, --local FILE")
   print("     File with local IDs")
   print(" -h, --help")
   print("     Print this help")
   

mfsin = None
flocal = None
outdir = None
prefix = ''
mutf = 'variants'
distf = 'matrix.csv'
inmsn = 'inmsn'
gmlf = 'tmp_msn.gml'
finalgml = 'msn.gml'
freport = 'msn_report'
writematrix = False
th = 90
maxiter = 100

try:
   opts, args = getopt.getopt(sys.argv[1:], "m:o:p:b:xi:l:h", ["msa=", "outdir=", "prefix=", "borderth=", "writematrix", "maxiter=", "local=", "help"])
except getopt.GetoptError:
   usage()
   sys.exit()
for opt, arg in opts:
   if opt in ('-m', '--msa'):
      mfsin = arg
   elif opt in ('-o', '--outdir'):
      outdir = arg
   elif opt in ('-p', '--prefix'):
      prefix = arg
   elif opt in ('-b', '--borderth'):
      th = int(arg)
   elif opt in ('-x', '--writematrix'):
      writematrix = True
   elif opt in ('-i', '--maxiter'):
      maxiter = int(arg)
   elif opt in ('-l', '--local'):
      flocal = arg
   elif opt in ('-h', '--help'):
      usage()
      sys.exit(0)
   else:
      usage()
      sys.exit(1)

if len(sys.argv[1:]) == 0:
   usage()
   sys.exit(1)
elif mfsin is None:
   usage()
   sys.exit(1)

if outdir is None:
   outdir = os.path.dirname(mfsin)
   if not outdir:
      outdir = '.'

if prefix:
   mutf = prefix + '-' + mutf
   distf = prefix + '-' + distf
   inmsn = prefix + '-' + inmsn
   gmlf = prefix + '-' + gmlf
   finalgml = prefix + '-' + finalgml
   freport = prefix + '-' + freport

matrix, mutations = libdist.read_msa(mfsin, th)
mfh = open(outdir + '/' + mutf, 'w')
for gid in mutations:
   mfh.write(gid + '\t' + str(set(mutations[gid].flatten())) + '\n')
mfh.close()

mat = libdist.compare4(matrix)
gids = list(matrix.keys())

if writematrix:
   df = pd.DataFrame(mat, index=gids, columns=gids)
   df.to_csv(outdir + '/' + distf)

Matrix(mat, gids, outdir + '/' + inmsn)

msn = MinimumSpanningNetwork(outdir + '/' + inmsn, outdir + '/' + mutf)
g = msn.create_graph(maxIter = maxiter)
msn.export_directed_graph(outdir + '/' + gmlf)

if flocal is None:
   GMLParser(outdir + '/' + gmlf, outdir + '/' + mutf, outdir + '/' + finalgml)
else:
   GMLParser(outdir + '/' + gmlf, outdir + '/' + mutf, outdir + '/' + finalgml, outdir + '/' + freport, flocal)

os.remove(outdir + '/' + inmsn)
os.remove(outdir + '/' + gmlf)