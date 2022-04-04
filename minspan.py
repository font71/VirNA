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
   print(" -p, --prefix STR")
   print("     The string to attach to every output files (default: \"\")")
   print(" -x, --matrix")
   print("     Dumps edit distance matrix")
   print(" -t, --borderth INT")
   print("     The multiple alignment will be trimmed at both ends using this value(default value 90)")
   print(" -i, --maxiter INT")
   print("     Maximum number of iterations to perform during MSN building")
   print(" -h, --help")
   print("     Print this help")
   

prefix = ''
mutf = 'variants'
distf = 'matrix.csv'
inmsn = 'inmsn'
gmlf = 'tmp_msn.gml'
finalgml = 'msn.gml'
writematrix = False
th = 90
maxiter = 100

try:
   opts, args = getopt.getopt(sys.argv[1:], "m:p:b:xi:h", ["msa=", "prefix=", "borderth=", "writematrix", "maxiter=", "help"])
except getopt.GetoptError:
   usage()
   sys.exit()
for opt, arg in opts:
   if opt in ('-m', '--msa'):
      mfsin = arg
   elif opt in ('-p', '--prefix'):
      prefix = arg
   elif opt in ('-b', '--borderth'):
      th = int(arg)
   elif opt in ('-x', '--writematrix'):
      writematrix = True
   elif opt in ('-i', '--maxiter'):
      maxiter = int(arg)
   elif opt in ('-h', '--help'):
      usage()
      sys.exit(0)
   else:
      usage()
      sys.exit(1)
if len(sys.argv[1:]) == 0:
   usage()
   sys.exit(1)

if prefix:
   mutf = prefix + '-' + mutf
   distf = prefix + '-' + distf
   inmsn = prefix + '-' + inmsn
   gmlf = prefix + '-' + gmlf
   finalgml = prefix + '-' + finalgml

matrix, mutations = libdist.read_msa(mfsin, th)
mfh = open(mutf, 'w')
for gid in mutations:
   mfh.write(gid + '\t' + str(set(mutations[gid].flatten())) + '\n')
mfh.close()

mat = libdist.compare4(matrix)
gids = list(matrix.keys())

if writematrix:
   df = pd.DataFrame(mat, index=gids, columns=gids)
   df.to_csv(distf)

Matrix(mat, gids, inmsn)

msn = MinimumSpanningNetwork(inmsn, mutf)
g = msn.create_graph(maxIter = maxiter)
msn.export_directed_graph(gmlf)

GMLParser(gmlf, mutf, finalgml)

os.remove(inmsn)
os.remove(gmlf)