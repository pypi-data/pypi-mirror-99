### FlowGradedComplex.py
### MIT LICENSE 2016 Shaun Harker
#
# Marcio Gameiro
# 2021-03-24

from pychomp2._chomp import *
from pychomp2.CondensationGraph import *
from pychomp2.StronglyConnectedComponents import *
from pychomp2.DirectedAcyclicGraph import *
from pychomp2.Poset import *

def FlowGradedComplex(complex, discrete_flow):
  """
  Overview:
    Given a complex and a graph on its top dimensional cells,
    produce a GradedComplex such that the preimage of a down set
    is the collection of cells in the closure of all the 
    associated top cells
  Inputs:
    complex    : a complex
    flow_graph : a function from vertices to out-adjacent vertices
  Algorithm:
    Apply strongly connected components algorithm and determine
    reachability relation among the strong components to learn
    a poset. Associated to each poset vertex is a collection of
    top cells. 
  """

  # Step 1. Compute the poset of strongly connected components
  
  vertices = [ cell for cell in complex(complex.dimension())]
  (dag, mapping) = CondensationGraph(vertices, discrete_flow)
  #poset = Poset(dag)

  # Step 2. Extend the mapping from top-cells to all cells
  # Basic idea: since the component indexing furnishes a linear
  #             extension of the poset, we assign each cell to 
  #             the minimum indexed poset which contains a top cell
  #             it is incident.


  # for cell in reversed(range(0,len(complex))):
  #   current_value = mapping[cell]
  #   for bd_cell in complex.boundary({cell}):
  #     mapping[bd_cell] = min(mapping.get(bd_cell,current_value), current_value)

  #num_nontop_cells = complex.size() - complex.size(complex.dimension())

  #valuation = lambda x : min([mapping[z] for z in complex.star(x) if z >= num_nontop_cells])

  grading = construct_grading(complex, lambda x : mapping[x] );
  return dag, GradedComplex(complex, grading) # lambda x : mapping[x])

  #return poset, chompy.GradedComplex(complex, lambda x : mapping[x])
