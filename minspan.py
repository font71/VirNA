#!/usr/bin/env python3

from libmat import libdist
from libmat.distance_matrix import Matrix
from libmat.msn2 import MinimumSpanningNetwork
from libmat.gml import GMLParser
import sys
import pandas as pd
import getopt
import os
import networkx as nx
from libmat.analyzeComponents import AnalyzeGraph


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
   print("     Maximum number of iterations to perform during MSN building (default: 100)")
   print(" -l, --local FILE")
   print("     File with local IDs")
   print(" -n, --ccth INT")
   print("     Minimum number of nodes of a connected component (default: 5)")
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
ccth = 5

# sys.argv.append('-m')
# sys.argv.append('out2/1_chosen_sequences_edited_NO_ID.fasta')
# sys.argv.append('-o')
# sys.argv.append('out2')
# sys.argv.append('-i')
# sys.argv.append('7')
try:
   opts, args = getopt.getopt(sys.argv[1:], "m:o:p:b:xi:l:n:h", ["msa=", "outdir=", "prefix=", "borderth=", "writematrix", "maxiter=", "local=", "ccth=", "help"])
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
   elif opt in ('-n', '--ccth'):
      ccth = int(arg)
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

Matrix(mat, gids, outdir + '/' + inmsn)

msn = MinimumSpanningNetwork(outdir + '/' + inmsn, outdir + '/' + mutf)
g = msn.create_graph(maxIter = maxiter)
msn.export_directed_graph(outdir + '/' + gmlf)

if flocal is None:
   gmlp = GMLParser(outdir + '/' + gmlf, outdir + '/' + mutf, outdir + '/' + inmsn, outdir + '/' + freport)
else:
   gmlp = GMLParser(outdir + '/' + gmlf, outdir + '/' + mutf, outdir + '/' + inmsn, outdir + '/' + freport, flocal)
nx.write_gml(gmlp.get_graph(), outdir + '/' + finalgml)

df = pd.DataFrame(mat, index=gids, columns=gids)
AnalyzeGraph(gmlp.get_graph(), df, ccth, gids, outdir + '/' + freport)

if writematrix:
#   df = pd.DataFrame(mat, index=gids, columns=gids)
   df.to_csv(outdir + '/' + distf)


os.remove(outdir + '/' + inmsn)
os.remove(outdir + '/' + gmlf)