#coding=utf-8
import networkx as nx
import igraph as ig
import numpy as np
from load_data import gml_data
gml_name='karate_club'

def get_modularity_method1(G,clustering):
    edges=G.edges()
    m=len(edges)
    degree_dict = G.degree()

    #clustering =nx.connected_components(G)

    ret = 0.0
    for c in clustering:
        for x in c:
            for y in c:
                if x <= y:
                    if (x, y) in edges:
                        aij = 1.0
                    else:
                        aij = 0.0
                else:
                    if (y, x) in edges:
                        aij = 1.0
                    else:
                        aij = 0
                tmp = aij - degree_dict[x] * degree_dict[y] * 1.0 / (2 * m)
                ret = ret + tmp
    ret = ret * 1.0 / (2 * m)
    return ret

def get_modularity_method2(G,clustering):
    edges=G.edges()
    m=len(edges)
    degree=G.degree()
    #clustering = nx.connected_components(G)
    ret = 0.0
    for c in clustering:
       bian=0
       for x in c:
           for y in c:
               if x<=y:
                   if (x,y) in edges:
                       bian=bian+1
               else:
                   if (y,x) in edges:
                       bian=bian+1
       duHe=0
       for x in c:
           duHe=duHe+degree[x]
       tmp=bian*1.0/(2*m)-(duHe*1.0/(2*m))*(duHe*1.0/(2*m))
       ret=ret+tmp
    return ret


def get_modularity_method3(G,clustering):
    k = nx.number_connected_components(G)
    #clustering = list(nx.connected_components(G))
    m = G.number_of_edges()
    edges = G.edges()
    e = np.zeros((k, k), np.float)

    for i in range(k):
        for j in range(k):
            bian = 0
            for x in clustering[i]:
                for y in clustering[j]:
                    if x < y:
                        if (x, y) in edges:
                            bian = bian + 1
                    else:
                        if (y, x) in edges:
                            bian = bian + 1
            if i == j:
                bian = bian / 2

            if i==j:
                e[i, j] = bian * 1.0 / m
            else:
                e[i, j] = bian * 0.5 / m

    a = np.zeros(k, np.float)
    for i in range(k):
        he = 0
        for j in range(k):
            he = he + e[i, j]
        a[i] = he
    QValue = 0
    for i in range(k):
        QValue = QValue + e[i, i] - a[i] * a[i]
    return QValue

def get_modularity_method4(G,clustering):
    r= nx.number_connected_components(G)
    #clustering = list(nx.connected_components(G))

    n=G.number_of_nodes()
    m=G.number_of_edges()

    S=np.mat(np.zeros((n,r)))
    for i in range(n):
        for j in range(r):
            if i in clustering[j]:
                S[i,j]=1
    A=nx.to_numpy_matrix(G)
    degree=nx.degree(G)
    B=np.mat(np.zeros((n,n)))
    for i in range(n):
        for j in range(n):
            B[i,j]=A[i,j]-(degree[i]*degree[j])/(2.0*m)

    return np.trace(S.T*B*S)/(2.0*m)

if __name__=='__main__':
    path = '../data/karate/karate.gml'
    nodes, edges = gml_data.load_gml_data(path)

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    #G = ig.Graph.Read_GML('%s.gml'%gml_name)
    # print get_modularity_method1(G)
    # print get_modularity_method2(G)
    # print get_modularity_method3(G)
    # print get_modularity_method4(G)
    #
    # G=ig.Graph.Read_GML('%s_new.gml'%gml_name)
    # verterclustering=ig.Graph.components(G)
    # print verterclustering
    list = [[0, 1, 2, 3, 7, 11, 12, 13, 17, 19, 21], [4, 5, 6, 10, 16], [23, 24, 25, 27, 28, 31],
            [8, 9, 14, 15, 18, 20, 22, 26, 29, 30, 32, 33]]
    print (get_modularity_method4(G,list))
    print (get_modularity_method1(G,list))
    print (get_modularity_method2(G,list))
    print (get_modularity_method3(G,list))

    # G = ig.Graph.Read_GML('%s_new.gml' % gml_name)
    # list=[0,0,0,0,1,1,1,0,3,3,1,0,0,0,3,3,1,0,3,0,3,0,3,2,2,2,3,2,2,3,3,2,3,3]
    # ig.VertexClustering(G,list)
    # clustering=ig.VertexClustering(G,list)
    #
    # print clustering.modularity
    # #G=clustering.subgraphs()
