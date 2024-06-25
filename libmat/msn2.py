# This is a sample Python script.
import ast
import json
from  igraph import Graph
# import math

class MinimumSpanningNetwork:
    def __init__(self,inFile, varFile = None):
        fh = open(inFile, "r")
        line = fh.readline().strip()
        self._weights = json.loads(line)
        line = fh.readline().strip()
        self._nodeids = json.loads(line)["nodes"]
        #print(self._nodeids)
        line = fh.readline().strip()
        self._identities = json.loads(line)
        line = fh.readline().strip()
        if len(line) > 0:
            self._lineages = json.loads(line)["lineages"]
        else:
            self._lineages = []
        #print(self._identities)
        #print(self._lineages)
        #exit(1)
        fh.close()
        self._Graph = Graph(directed = False)
        self.variants = dict()
        self.annotations = dict()
        if varFile != None:
            vFile = open(varFile, 'r')
            for line in vFile:
                line = line.strip()
                els = line.split('\t')
                data = els[0].split("/")
                if len(data) > 2:
                    self.annotations[data[1]] = []
                    for i in range(len(data)):
                        if i != 1:
                            self.annotations[data[1]].append(data[i])

                if els[1] != 'set()':
                    vars = ast.literal_eval(els[1])
                else:
                    vars = set()
                self.variants[data[1]] = vars
            vFile.close()
            # print(self.annotations)


    def add_all_edges(self, level = 0):

        edges = self._weights.get(str(level), None)
        if edges != None:

            for e in edges:
                eType = self.check_edge_type(e[0], e[1])
                if eType == 'FWD':
                    self._Graph.add_edge(e[0],
                                         e[1],
                                         levels=level,
                                         Etype=eType,
                                         sourceNM=self._nodeids[e[0]],
                                         sourceID=e[0],
                                         targetNM = self._nodeids[e[1]],
                                         targetID = e[1]
                    )
                elif eType == 'REV':
                    self._Graph.add_edge(e[0],
                                         e[1],
                                         levels=level,
                                         Etype=eType,
                                         sourceNM=self._nodeids[e[1]],
                                         sourceID=e[1],
                                         targetNM = self._nodeids[e[0]],
                                         targetID = e[0]
                                         )
                # MOD LUCA: 29/03
                #else:
                #    self._Graph.add_edge(e[0],
                #                         e[1],
                #                         levels=level,
                #                         Etype=eType,
                #                         sourceNM=self._nodeids[e[0]],
                #                         sourceID=e[0],
                #                         targetNM=self._nodeids[e[1]],
                #                         targetID=e[1]
                #                         )
                # END MOD LUCA: 29/03

                    #self._Graph.add_edge(e[1], e[0], levels=level, Etype=eType)

    #returns the orientation of the edge (possible cases are:FWD, REV and BOTH)
    # FWD: variants of e1 are entirely contained in variants of e2
    # REV: variants of e2 are entirely contained in variants of e1
    # BOTH: else (in this case both edges e1 <--> e2 are added to the graph)
    def check_edge_type(self, e1, e2):
        v1 = self.variants[self._nodeids[e1]]
        v2 = self.variants[self._nodeids[e2]]
        inter = v1.intersection(v2)
        if inter == v1:
            return "FWD"
        elif inter == v2:
            return "REV"
        else:
            return "BOTH"
    def add_edges(self, level = 0):
        def __merge_components(cc, i1, i2):
            cc[i1] = cc[i1].union(cc[i2])
            #cc[i1].union(cc[i2])
            cc[i2] = set()
            #print("here")
        def __same_component(cc, n1, n2, merge = True):
            i1 = -1
            i2 = -1
            for ind in range(len(cc)):
                if n1 in cc[ind]:
                    i1 = ind
                if n2 in cc[ind]:
                    i2 = ind

                if i1 != -1 and i2 != -1:
                    break
            ret = i1 == i2
            if merge and not ret:
                __merge_components(cc, i1, i2)
            #exit(1)
            return ret

        CC = [ set(x) for x in list(self._Graph.components()) ]


        if len(CC) == 1:
            return False
        edges = self._weights.get(str(level), None)

        if edges != None:
            #if "levels" not in self._Graph.es:
            #    print("added levels")
            #    self._Graph.es["levels"] = []
            #edges2add = []
            for e in edges:
                #if self._Graph.shortest_paths(source=e[0], target=e[1])[0][0] == math.inf:

                #EDITED by Luca (01/02/2023)
                eType = self.check_edge_type(e[0], e[1])
                if eType == "BOTH":
                    continue

                # END EDIT Luca
                
                # if not __same_component(CC, e[0], e[1], merge = True):
                if not __same_component(CC, e[0], e[1], merge = False):
                    #Removed by Luca (01/02/2023)
                    #eType = self.check_edge_type(e[0], e[1])

                    if eType == 'FWD':
                        #edges2add.append((e[0], e[1]))
                        self._Graph.add_edge(e[0],
                                             e[1],
                                             levels=level,
                                             Etype=eType,
                                             sourceNM=self._nodeids[e[0]],
                                             sourceID=e[0],
                                             targetNM=self._nodeids[e[1]],
                                             targetID=e[1]
                                             )
                        #print(self._Graph)
                    elif eType == 'REV':
                        #edges2add.append((e[1], e[0]))
                        self._Graph.add_edge(e[0],
                                             e[1], levels=level,
                                             Etype=eType,
                                             sourceNM=self._nodeids[e[1]],
                                             sourceID=e[1],
                                             targetNM=self._nodeids[e[0]],
                                             targetID=e[0]
                                             )
                    # MOD LUCA: 29/03
                    #else:
                    #    #edges2add.append((e[0], e[1]))
                    #    #edges2add.append((e[1], e[0]))
                    #    self._Graph.add_edge(e[0],
                    #                         e[1],
                    #                         levels=level,
                    #                         Etype=eType,
                    #                         sourceNM=self._nodeids[e[0]],
                    #                         sourceID=e[0],
                    #                         targetNM=self._nodeids[e[1]],
                    #                         targetID=e[1]
                    # )
                        #self._Graph.add_edge(e[1], e[0], levels=level, Etype=eType)
                        #print("EDGE: {}".format(e))
                        #self._Graph.es[e]["type"] = "unrelated"
                    #print("Adding edge: {} - {}/{} -> {}".format(self._nodeids[e[0]],eType,level, self._nodeids[e[1]]))
                    #print("Variants {}: {}".format(self._nodeids[e[0]],self.variants[self._nodeids[e[0]]]))
                    #print("Variants {}: {}".format(self._nodeids[e[1]], self.variants[self._nodeids[e[1]]]))

            #print("NEW: ", CC)
            #print(len(CC))




        return True

    def export_directed_graph(self, outFile):
        tmpG = Graph(directed = True)

        for v in self._Graph.vs:
            #print(v)
            #print(v.index)
            #print(v.attributes())
            #print(self._nodeids[v.index])
            tmpG.add_vertex(v.index)

            for att in v.attributes():
                tmpG.vs[v.index][att] = v.attributes()[att]
        tmpG.vs["name"] = self._nodeids
        for e in self._Graph.es:
            #print("EDGE: {}".format(e))
            #print("{} --> {} {}".format(e.source, e.target, e.attributes()))
            nSource = e.attributes()["sourceID"]
            nTarget = e.attributes()["targetID"]
            tmpG.add_edge(nSource, nTarget)
            eid = tmpG.get_eid(nSource, nTarget)
            for attr in e.attributes():
                tmpG.es[eid][attr] = e.attributes()[attr]

                tmpG.es[attr] = self._Graph.es.get_attribute_values(attr)

        tmpG.write_gml(outFile)

    def export_graph(self, outFile):

            self._Graph.write_gml(outFile)
            #self._Graph.write(outFile)

    def get_distances(self):
        return self._weights

    def get_nodeids(self):
        return self._nodeids

    def create_graph(self, maxIter = 30):
        self._Graph.add_vertices(len(self._nodeids))

        #self.add_all_edges(level = 0)
        for i in range(1,maxIter):

            print("Level {}".format(i))
            multipleCC = self.add_edges(level=i)
            if not multipleCC:
                break
        self._Graph.vs["name"] = self._nodeids
        if len(self._lineages) > 0:
            self._Graph.vs["lineage"] = self._lineages
        ident_sizes = [0 for x in self._nodeids]
        identical_nodes = ["" for x in self._nodeids]
        locations = [self.annotations[x][0] for x in self._nodeids]
        dates = [self.annotations[x][1] for x in self._nodeids]
        # variants_tmp = [self.variants[x] for x in self._nodeids]
        # variants = [",".join(list(x)) for x in variants_tmp]
        for x in self._identities:
            ident_sizes[int(x)] = len(self._identities[x])
            identical_nodes[int(x)] = ";".join(self._identities[x])
        self._Graph.vs["N_identical"] = ident_sizes
        # self._Graph.vs["identical_nodes"] = identical_nodes
        self._Graph.vs["location"] = locations
        self._Graph.vs["collection_date"] = dates
        # self._Graph.vs["variants"] = variants



        return self._Graph

    def get_degree(self):
        return self._Graph.degree()

    def nodeid(self, index):
        return self._nodeids[index]

    def print_node_stats(self, xtimes_hub = 10, eb_ratio = 0.95):
        N = len(self._Graph.vs)
        print("The graph has {} nodes".format(N))
        degrees = self.get_degree()

        M = []
        m = []
        mval = N
        Mval = 0
        s = 0
        mean_degree = sum(degrees)/N
        hubs = []
        print("The mean degree is {:.3f}".format(mean_degree))
        for i in range(len(degrees)):
            if degrees[i] >= Mval:
                if degrees[i] == Mval:
                    M.append(self.nodeid(i))
                else:
                    M = [self.nodeid(i)]
                    Mval = degrees[i]
            if degrees[i] <= mval:
                if degrees[i] == mval:
                    m.append(self.nodeid(i))
                else:
                    m = [self.nodeid(i)]
                    mval = degrees[i]
            if degrees[i] > xtimes_hub*mean_degree:
                hubs.append(self.nodeid(i))
        #compute edge-betweeness (i.e. the number of shortest paths going through each edge)
        edge_betweenness = self._Graph.edge_betweenness()
        mean_eb = sum(edge_betweenness)/len(edge_betweenness)
        max_edges = [self._Graph.es[idx].tuple for idx, eb in enumerate(edge_betweenness) if eb > eb_ratio*mean_eb]
        print("The {} node(s) with max degree ({}): {}".format(len(M), Mval, M))
        print("The {} node(s) with min degree ({}): {}".format(len(m), mval, m))
        print("There are {} hubs (degree > {}*mean = {:.2f}): {}".format(len(hubs),xtimes_hub, xtimes_hub*mean_degree, hubs))
        print("There are {} edges with edge betweeness > {}% mean eb ({})".format(len(max_edges), eb_ratio*100, mean_eb*eb_ratio))
        for e in max_edges:
            print(" - {} -> {}".format(self.nodeid(e[0]), self.nodeid(e[1])))

    def __init2__(self, inFile):
        fh = open(inFile, "r")
        line = fh.readline().strip()
        self.weights = ast.literal_eval(line)
        line = fh.readline().rstrip()
        self.gids = ast.literal_eval(line)
        fh.close()
        #print(self.weights)
        ostr = "{"
        for el in self.weights:
            ostr += "\"{}\" : {}".format(str(el), str(self.weights[el]))
        ostr += "}"
        print(ostr)
        #print(gids)
        #return weights, gids



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   import sys

#    MSN = MinimumSpanningNetwork(sys.argv[1], sys.argv[2])
#    G = MSN.create_graph(maxIter = 100)
#    MSN.export_directed_graph(sys.argv[3])
   MSN = MinimumSpanningNetwork('SEQS_1-inmsn', 'SEQS_1-variants')
   G = MSN.create_graph(maxIter = 100)
   MSN.export_directed_graph('out.gml')
