import numpy as np
import pandas as pd
from igraph import *
import json
import sys


class Matrix:
   def __init__(self, mat, gids, inmsn):
      distances = self.get_distances(mat, gids)
      if 0 in distances:
         equalvs = self.get_equal_vs(distances[0], gids)
      else:
         equalvs = {}

      noeqgids = list()
      gidnoeqdct = dict()

      n = 0
      for i in range(len(gids)):
         if not i in equalvs:
            gid = gids[i]
            noeqgids.append(gid)
            gidnoeqdct[gid] = n
            n += 1

      eqdct = dict()
      for i in equalvs:
         v = gids[equalvs[i]]
         nv = gidnoeqdct[v]
         if nv in eqdct:
            eqdct[nv].append(gids[i])
         else:
            eqdct[nv] = [gids[i]]

      noeqdist = dict()
      edgedone = set()
      for i in range(1, max(distances.keys()) + 1):
         edges = list()
         if i in distances:
            for edge in distances[i]:
               v1 = edge[0]
               v2 = edge[1]
               if gids[v1] in gidnoeqdct:
                  v1 = gidnoeqdct[gids[v1]]
               else:
                  v1 = gidnoeqdct[gids[equalvs[v1]]]
               if gids[v2] in gidnoeqdct:
                  v2 = gidnoeqdct[gids[v2]]
               else:
                  v2 = gidnoeqdct[gids[equalvs[v2]]]
               
               # if not (v1, v2) in edgedone: #and not (v2, v1) in edgedone:
               if not (v1, v2) in edgedone and not (v2, v1) in edgedone: # write only half of the sqare matrix
                  edges.append([v1, v2])
                  edgedone.add((v1, v2))
               
            noeqdist[i] = edges
         
      # tnoeqgids = list()
      # for n in noeqgids:
      #    tnoeqgids.append(n.split('/')[1])
      # noeqgids = tnoeqgids
      # teqdct = dict()
      # for k in eqdct:
      #    teqdct[k] = list()
      #    for kk in eqdct[k]:
      #       teqdct[k].append(kk.split('/')[1])
      # eqdct = teqdct

      fh = open(inmsn, 'w')
      fh.write(json.dumps(noeqdist) + '\n')
      fh.write('{\"nodes\" : ' + json.dumps(noeqgids) + '}\n')
      fh.write(json.dumps(eqdct) + '\n')
      fh.close()

   def get_distances(self, mat, gids):
      edges = dict()
      d = len(gids)

      for i in range(d):
         for j in range(i + 1, d):
            dist = mat[i][j]
            if dist in edges:
               edges[dist].append([i, j])
            else:
               edges[dist] = [[i, j]]
      return edges

   def get_equal_vs(self, edges=list, gids=list):
      equalvs = dict()
      
      gt = Graph(edges)
      clusters = gt.clusters()

      for cluster in clusters:
         if len(cluster) > 1:
            for v in cluster[1:]:
               equalvs[v] = cluster[0]
      return equalvs

if __name__ == "__main__":
   # Mutations('MSA_DATA/Edited_United_Kingdom_15D/Edited_United_Kingdom_27.fasta', 'distance_matrix_27.csv')
   Matrix(sys.argv[1])
