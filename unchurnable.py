""" Input: A file containing graphs. The format accepted is g6.
    Output: A list of graphs G (number of nodes followed by list of edges) such that G is not in X\cup Y and G-V_ell and G-V_h are in Y. 
    See the paper "Incompressibility of H-free edge modification problems: Towards a dichotomy" by Daniel Marx and R. B. Sandeep.
    Usage: python2 unchurnable.py input.g6 output.txt
    Input can be found at https://users.cecs.anu.edu.au/~bdm/data/graphs.html
"""

import networkx as nx
import sys

def read_graph6(path):
    """Read simple undirected graphs in graph6 format from path.
    """
    with open(path, "rb") as infile:
        for line in infile:
            line = line.strip()
            if not len(line):
                continue
            yield nx.from_graph6_bytes(line)

def isComplete(G):
    """Is G a complete graph?
    """
    n = G.number_of_nodes()
    m = G.number_of_edges()
    if m == n*(n-1)/2:
        return True
    return False

def isRegular(G):
    """Is G a regular graph?
    """
    degrees = G.degree()
    V = G.nodes()
    degreeSet = set()
    for (u,d) in degrees:
        degreeSet.add(d)
        if len(degreeSet) > 1:
            return False
    return True

def inY(G):
    """Is G in Y?
    """
    C4 = nx.cycle_graph(4)
    if G.number_of_nodes() <=4:
        if nx.is_isomorphic(G, C4):
            return False # C_4
        if G.number_of_edges()==2 and isRegular(G):
            return False # 2K_2
        return True
    if G.number_of_edges() <= 1:
        return True
    if isComplete(G):
        return True
    return False

def inXorY(G, Gbar):
    """Is G in X U Y?
    """

    P5 = nx.path_graph(5) # A path on 5 vertices
    if G.number_of_nodes() <= 4:
        return True # in Y (except 2K_2 and C_4 - in X)
    if G.number_of_edges() <= 1:
        return True # in Y
    if isRegular(G): # in X (except for empty and complete which are in Y)
        return True
    if nx.node_connectivity(G) >= 3:
        return True # in X (except for complete G - in Y)
    if nx.node_connectivity(Gbar) >= 3:
        return True # in X (except for empty G - in Y)
    if G.number_of_nodes() == 5:
        if nx.is_isomorphic(G, P5):
            return True # in X
        if nx.is_isomorphic(Gbar, P5):
            return True # in X
    return False

def minmaxDegree(G):
    """ Get minimum degree and maximum degree of G
    """
    mind = G.number_of_nodes()
    maxd = -1
    for v in G.nodes():
        if mind > G.degree[v]:
            mind = G.degree[v]
        if maxd < G.degree[v]:
            maxd = G.degree[v]
    return mind, maxd

def getMinmaxVertices(G, mind, maxd):
    """ Get list of vertices with mindegree (mind) and list of vertices with maxdegree (maxd). 
    Assumes mind != maxd.
    """
    minV = []
    maxV = []
    for v in G.nodes():
        if G.degree[v] == mind:
            minV.append(v)
        elif G.degree[v] == maxd:
            maxV.append(v)
    return minV, maxV

if len(sys.argv) < 2:
    print "Usage: python2 unchurnable.py input.g6 output.txt"
else:
    unChurnable = []
    for G in read_graph6(sys.argv[1]):
        Gbar = nx.complement(G)
        if inXorY(G, Gbar):
            continue                   # not eligible for churning   
        mind, maxd = minmaxDegree(G)
        minV, maxV = getMinmaxVertices(G, mind, maxd)
        Gcopy1 = G.copy()
        Gcopy2 = G.copy()
        Gcopy1.remove_nodes_from(minV) # delete lowest degree vertices from a copy
        Gcopy2.remove_nodes_from(maxV) # delete highest degree vertices from a copy
        if inY(Gcopy1) and inY(Gcopy2): # if both the resultant graphs are in Y
            unChurnable.append(G)      # add it to the list of unchurnable graphs 
outputf = sys.argv[2]
of = open(outputf, "w")
# write the unchurnable graphs into an output file
i = 1
for G in unChurnable:
    of.write("Graph "+str(i)+"\n")
    i = i + 1
    of.write(str(G.number_of_nodes())+" "+str(G.number_of_edges())+"\n")
    for u,v in G.edges():
        of.write(str(u)+" "+str(v)+"\n")
of.close()

