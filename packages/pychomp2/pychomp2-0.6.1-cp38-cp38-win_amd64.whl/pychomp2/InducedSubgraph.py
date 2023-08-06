# InducedSubgraph.py
# Shaun Harker
# MIT LICENSE
# 2018-03-12
#
# Marcio Gameiro
# 2021-03-24

from pychomp2.DirectedAcyclicGraph import *
from pychomp2.Poset import *

def InducedSubgraph( G, predicate ):
    result = DirectedAcyclicGraph()
    S = set([v for v in G.vertices() if predicate(v)])
    for v in S:
        result.add_vertex(v)
    for v in S:
        for u in G.adjacencies(v):
            if u in S and u != v:
                result.add_edge(v,u)
    return result

def InducedPoset( G, predicate ):
    result = DirectedAcyclicGraph()
    S = set([v for v in G.vertices() if predicate(v)])
    for v in S:
        result.add_vertex(v)
    for v in S:
        for u in G.descendants(v):
            if u in S and u != v:
                result.add_edge(v,u)
    return Poset(result)
