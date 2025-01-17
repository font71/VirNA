import networkx as nx
import pandas as pd
import sys
import os.path


class AnalyzeGraph:
    def __init__(self, g: nx.DiGraph, df: pd.DataFrame, numth, gids, freport):
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
            fh.write(mincc[0] + '\t' + mincc[1] + '\t' + str(mincc[2]) + '\t' + str(minccdict[mincc]) + '\n')

        fh.close()

    def analyze(self, cc, df, indx):
        buffer = ('', '', sys.maxsize)

        for node in cc:
            mindist = ('', '', sys.maxsize)

            i = indx[node]
            for j in df[node]:
                dist = df.iloc[i, j]
                if dist == -1:
                    dist = df.iloc[j, i]
                if dist < mindist[2]:
                    mindist = (node, df.index[j], dist)

            if mindist[2] < buffer[2]:
                buffer = mindist

        return buffer
            