import networkx as nx
import datetime
import json
import ast


class GMLParser:
    def __init__(self, fgml, mutf, finmsn, freport, flocal=None):
        nodedates = dict()
        global g
        
        self.meta, self.mutations = self.read_mutations(mutf)
        self.identicalnodes = self.read_inmsn(finmsn)

        g = nx.read_gml(fgml, label='name', destringizer=str)

        if flocal is None:
            message = list()

            for n in g.nodes:
                if len(g.in_edges(n)) > 1:
                    m = list()
                    for n1, n2 in g.in_edges(n):
                        m.append(n1 + '->' + n2)
                    message.append(n + ' recombination event\t' + '; '.join(m))
                if n in self.identicalnodes:
                # if g.nodes[n]['identicalnodes']:
                    # identicalnodes = g.nodes[n]['identicalnodes'].split(';')
                    metaslice = {self.meta[x] for x in self.identicalnodes[n]}
                    metaslice = sorted(metaslice, key=lambda x: x[2])
                    dp = '; '.join([','.join((tup1 , tup2, tup3.strftime('%Y-%m-%d'))) for (tup1, tup2, tup3) in metaslice])
                    g.nodes[n]['identicalnodes'] = dp
                g.nodes[n]['variants'] = ','.join(self.mutations[n])
            
            if len(message) > 0:
                fh = open(freport, 'w')
                for line in message:
                    fh.write(line + '\n')
                fh.close()
        else:
            self.local = self.read_local(flocal)
            edges = list(g.edges(data=True))
            
            fh = open(freport, 'w')

            done = set()
            buffer = set()
            for e in edges:
                srcid = e[2]['sourceNM']
                if srcid not in buffer:
                    if len(g.in_edges(srcid)) > 1:
                           message = list()
                           for n1, n2 in g.in_edges(srcid):
                               message.append(n1 + '->' + n2)
                           fh.write(srcid + ' recombination event\t' + '; '.join(message) + '\n')
                           buffer.add(srcid)
                source = g.nodes[srcid]
                if 'variants' not in source:
                    source['variants'] = ','.join(self.mutations[srcid])
                if not srcid in nodedates:
                    nodedates[srcid] = self.sort_date(source, srcid)

                trgid = e[2]['targetNM']
                if trgid not in buffer:
                    if len(g.in_edges(trgid)) > 1:
                           message = list()
                           for n1, n2 in g.in_edges(trgid):
                               message.append(n1 + '->' + n2)
                           fh.write(trgid + ' recombination event\t' + '; '.join(message) + '\n')
                           buffer.add(trgid)

                target = g.nodes[trgid]
                if not trgid in nodedates:
                    nodedates[trgid] = self.sort_date(target, trgid)
                if 'variants' not in target:
                    target['variants'] = ','.join(self.mutations[trgid])

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
#        nx.write_gml(g, outgml)

    def sort_date(self, node, nodeid):
        if nodeid in self.identicalnodes:
        # if node['identicalnodes']:
                loc = ''
                
                # identicalnodes = node['identicalnodes'].split(';')
                identn = self.identicalnodes[nodeid]

                c = 0
                for n in identn:
                    if n in self.local:
                        c += 1

                if len(identn) == c and nodeid in self.local:
                    loc = 'local'
                elif c == 0 and not nodeid in self.local:
                    loc = 'ext'
                else:
                    loc = 'mixed'

                metaslice = {self.meta[x] for x in identn}
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
        mutations = dict()

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
            mutations[hd[1]] = list(ast.literal_eval(data[1]))
        fh.close()
        
        return meta, mutations
    
    def read_local(self, floc):
        loc = set()
        fh = open(floc)
        for line in fh:
            line = line.rstrip()
            loc.add(line)
        fh.close()
        return loc

    def read_inmsn(self, finmsn):
        identicalnodes = dict()

        fh = open(finmsn)
        for i, line in enumerate(fh):
            if i == 1:
                line = line.strip()
                nn = json.loads(line)['nodes']
            elif i == 2:
                line = line.strip()
                ident= json.loads(line)
        fh.close()

        for i in range(len(nn)):
            if (str(i)) in ident:
                identicalnodes[nn[i]] = ident[str(i)]

        return identicalnodes

    def get_graph(self):
        return g
    
if __name__ == "__main__":
    GMLParser('../out/tn-tmp_msn.gml', '../out/tn-variants', '../out/tn-inmsn', '../out/tn-msn.gml', '../out/report', '../local')
    # GMLParser('../out/33-tmp_msn.gml', '../out/33-variants', '../out/33-inmsn', '../out/33-msn.gml')