import networkx as nx
import datetime


class GMLParser:
    def __init__(self, fgml, mutf, outgml):
        meta = self.read_mutations(mutf)

        g = nx.read_gml(fgml, label='name')
        for n in g.nodes:
            if g.nodes[n]['identicalnodes']:
                identicalnodes = g.nodes[n]['identicalnodes'].split(';')
                metaslice = {meta[x] for x in identicalnodes}
                metaslice = sorted(metaslice, key=lambda x: x[2])
                dp = '; '.join([','.join((tup1 , tup2, tup3.strftime('%Y-%m-%d'))) for (tup1, tup2, tup3) in metaslice])
                g.nodes[n]['identicalnodes'] = dp
        nx.write_gml(g, outgml)

    def read_mutations(self, mutf):
        fh = open(mutf)
        meta = dict()

        for line in fh:
            line = line.rstrip()
            data = line.split('\t')

            hd = data[0].split('/')
            dd = hd[2].split('-')
            if len(dd) == 1:
                date = datetime.datetime.strptime(dd[0], '%Y')
            elif len(dd) == 2:
                date = '-'.join(dd)
                date = datetime.datetime.strptime(date, '%Y-%m')
            elif len(dd) == 3:
                date = '-'.join(dd)
                date = datetime.datetime.strptime(date, '%Y-%m-%d')

            meta[hd[1]] = (hd[1], hd[0], date)
        return meta

if __name__ == "__main__":
    GMLParser('msn.gml', 'variants')