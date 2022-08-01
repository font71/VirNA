import networkx as nx
import datetime


class GMLParser:
    def __init__(self, fgml, mutf, outgml, freport=None, flocal=None):
        nodedates = dict()

        self.meta = self.read_mutations(mutf)

        g = nx.read_gml(fgml, label='name', destringizer=str)

        if flocal is None:
            for n in g.nodes:
                if g.nodes[n]['identicalnodes']:
                    identicalnodes = g.nodes[n]['identicalnodes'].split(';')
                    metaslice = {self.meta[x] for x in identicalnodes}
                    metaslice = sorted(metaslice, key=lambda x: x[2])
                    dp = '; '.join([','.join((tup1 , tup2, tup3.strftime('%Y-%m-%d'))) for (tup1, tup2, tup3) in metaslice])
                    g.nodes[n]['identicalnodes'] = dp
        else:
            self.local = self.read_local(flocal)
            edges = list(g.edges(data=True))
            
            fh = open(freport, 'w')

            done = set()
            for e in edges:
                srcid = e[2]['sourceNM']
                source = g.nodes[srcid]
                if not srcid in nodedates:
                    nodedates[srcid] = self.sort_date(source, srcid)

                trgid = e[2]['targetNM']
                target = g.nodes[trgid]
                if not trgid in nodedates:
                    nodedates[trgid] = self.sort_date(target, trgid)

                if nodedates[srcid]['location'] == 'mixed':
                    if not srcid in done:
                        pl1 = self.meta[srcid][1] + '. ' + self.meta[srcid][2].strftime("%Y-%d-%m")
                        pl2 = self.meta[nodedates[srcid]['startnode']][1] + ', ' + self.meta[nodedates[srcid]['startnode']][2].strftime("%Y-%d-%m")
                        if self.meta[srcid][2] <= self.meta[nodedates[srcid]['startnode']][2]:
                            fh.write(srcid + ' (' + pl1  + ') -> ' + nodedates[srcid]['startnode'] + ' (' + pl2  + ')' + '\tExit point mixed\n')
                        else:
                            fh.write(nodedates[srcid]['startnode'] + ' (' + pl2  + ')' + ' -> ' + srcid + ' (' + pl1  + ')' + '\tEntry point mixed\n')
                        done.add(srcid)

                if nodedates[srcid]['location'] == 'ext' and nodedates[trgid]['location'] == 'local':
                    pl1 = self.meta[srcid][1] + ', ' + self.meta[srcid][2].strftime("%Y-%d-%m")
                    pl2 = self.meta[trgid][1] + ', ' + self.meta[trgid][2].strftime("%Y-%d-%m")
                    if self.meta[srcid][2] <= self.meta[nodedates[trgid]['startnode']][2]:
                        fh.write(srcid  + ' (' + pl1  + ') -> ' + trgid + ' (' + pl2  + ')' + '\tEntry point\n')
                    else:
                        fh.write(srcid + ' (' + pl1  + ') -> ' + trgid + ' (' + pl2  + ')' + '\tMay be an entry point, but dates are not congruents\n')

                if nodedates[srcid]['location'] == 'local' and nodedates[trgid]['location'] == 'ext':
                    pl1 = self.meta[srcid][1] + ', ' + self.meta[srcid][2].strftime("%Y-%d-%m")
                    pl2 = self.meta[trgid][1] + ', ' + self.meta[trgid][2].strftime("%Y-%d-%m")
                    if self.meta[srcid][2] <= self.meta[nodedates[trgid]['startnode']][2]:
                        fh.write(srcid + ' (' + pl1  + ') -> ' + trgid + ' (' + pl2  + ')' + '\tExit point\n')
                    else:
                        fh.write(srcid + ' (' + pl1  + ') -> ' + trgid + ' (' + pl2  + ')' + '\tMay be an exit point, but date are not congruents\n')
                
            fh.close()
        nx.write_gml(g, outgml)

    def sort_date(self, node, nodeid):
        if node['identicalnodes']:
                loc = ''
                
                identicalnodes = node['identicalnodes'].split(';')

                c = 0
                for n in identicalnodes:
                    if n in self.local:
                        c += 1

                if len(identicalnodes) == c and nodeid in self.local:
                    loc = 'local'
                elif c == 0 and not nodeid in self.local:
                    loc = 'ext'
                else:
                    loc = 'mixed'

                metaslice = {self.meta[x] for x in identicalnodes}
                metaslice = sorted(metaslice, key=lambda x: x[2])

                dp = '; '.join([','.join((tup1 , tup2, tup3.strftime('%Y-%m-%d'))) for (tup1, tup2, tup3) in metaslice])
                node['identicalnodes'] = dp
                return {'startnode': metaslice[0][0], 'endnode': metaslice[-1][0], 'location': loc}

        if nodeid in self.local:
            loc = 'local'
        else:
            loc = 'ext'
        return {'startnode': nodeid, 'endnode': nodeid, 'location': loc}

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
    
    def read_local(self, floc):
        loc = set()
        fh = open(floc)
        for line in fh:
            line = line.rstrip()
            loc.add(line)
        fh.close()
        return loc

if __name__ == "__main__":
    GMLParser('../b1_tn-tmp_msn.gml', '../b1_tn-variants', '../prova.gml', '../local', '../report')