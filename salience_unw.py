
# coding: utf-8


"""A Python module for extracting the salient links of a graph,
   as defined by Grady, D., Thiemann, C., and Brockmann, D. (2012).
"""


#    Copyright (C) 2016 by
#    Iacopo Iacopini <iacopini.iacopo@gmail.com>
#    All rights reserved.
#    BSD license.

#    Unweighted version and bug-fixing by Giacomo Roversi <giacomo.roversi@edu.unife.it>

import networkx as nx
from networkx.utils import not_implemented_for
import numpy as np

__all__ = ['salience']

@not_implemented_for('directed')
@not_implemented_for('multigraph')
def _SPT(G, r):
    """Returns the shortest-path tree (SPT) T(r) for a fixed reference node r of the graph G (see [1]).
        
        Args
        ----
        G: NetworkX graph
        
        r: node
            The reference node belonging to the graph G.
            The SPT summarizes the most effective routes from r to the rest of the network.
             
        Returns
        -------
        T: numpy.ndarray
            T(r) is a symmetric N × N matrix with elements tij ( r ) = 1 if the link ( i , j ) is part of
            at least one of the shortest paths and tij ( r ) = 0 if it is not. 
            
        References
        ----------    
        .. [1] Grady, Daniel, Christian Thiemann, and Dirk Brockmann.
           "Robust classification of salient links in complex networks."
           Nature communications 3 (2012): 864.

    """
    
    Gn = nx.convert_node_labels_to_integers(G)
    N = Gn.order()
    T = np.zeros((N,N))
    
    paths=nx.shortest_path(Gn,source=r)
    #each path is a dictionary with key: r and value:the list of nodes in the path
    
    #Filling T based on the presence of a link in at least one of the shortest paths
    for k, path in paths.items(): 
        for i in range(len(path)-1):
            T[path[i]][path[i+1]]=1 #updating the matrix T because there is a link
    return T

def salience(G):
    """Returns the salience matrix of a graph G, defined as the average shortest-path tree (see [1]).
        
        Args
        ----
        G: NetworkX graph
           
        Returns
        -------
        S: numpy.ndarray
            S is the salience of a network G, as a lienar superposition of all the shortest-path trees.
        
        References
        ----------    
        .. [1] Grady, Daniel, Christian Thiemann, and Dirk Brockmann.
           "Robust classification of salient links in complex networks."
           Nature communications 3 (2012): 864.

    """
    
    N = G.order()
    S = np.zeros((N,N))
   
    Gn = nx.convert_node_labels_to_integers(G)
    for n in Gn.nodes():
      S = S + _SPT(G,n)
    S = 1.*S/N
    return S    

