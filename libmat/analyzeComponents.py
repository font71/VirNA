import networkx as nx
import pandas as pd
import sys
import os.path


class AnalyzeGraph:
    def __init__(self, g: nx.DiGraph, df: pd.DataFrame, numth, maxdist, gids, freport):
        indx = dict(zip(gids, list(range(len(gids)))))
        minccdict = dict()
        header = '################Isolated Nodes Analysis#################################\n'

        for cc in nx.connected_components(g.to_undirected()):
            if len(cc) <= numth:
                mincomp = self.analyze(cc, df, indx)
                minccdict[mincomp] = list(cc)
        
        if os.path.isfile(freport):
            header = '\n' + header

        fh = open(freport, 'a')
        fh.write(header)
        
        fh.write('Node\tNode at min HD\tHD\tConnected Component Nodes\n')
        for mincc in minccdict:
            if mincc[2] <= maxdist:
                fh.write(mincc[0] + '\t' + mincc[1] + '\t' + str(mincc[2]) + '\t' + str(minccdict[mincc]) + '\n')

        fh.close()

    def analyze(self, cc, df, indx):
        mindist = ('', '', sys.maxsize)

        for node in cc:
            i = indx[node]
            for j in range(len(indx)):
                if i == j:
                    continue
                dist = df.iloc[i, j]
                if dist == -1:
                    dist = df.iloc[j, i]
                if dist < mindist[2]:
                    mindist = (node, df.index[j], dist)

        return mindist
            