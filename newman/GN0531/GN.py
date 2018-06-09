#coding=utf-8
from __future__ import division
import igraph as ig
import networkx as nx
import numpy as np
import math
import csv
import shutil
import os.path
import cPickle as pickle

order='01'

gml_name = './benchmark%s/network%s'%(order,order)

def getNMI_A(filename,delimiter):
    community_list=[]
    reader = csv.reader(open('%s.txt'%filename), delimiter=delimiter)
    for line in reader:
        community_list.append(int(line[1]))
    return np.array(community_list)
A=getNMI_A('./benchmark%s/community_network%s'%(order,order),'	')

def draw_graph(G,filename,layout):
    clustering=G.components()
    print clustering
    covers = clustering.as_cover()  # 转点覆盖

    n = len(covers)
    pal = ig.ClusterColoringPalette(n)
    i = 0
    for li in covers:
        for node in li:
            G.vs[node]['color'] = pal.get(i)
        i += 1
    ig.plot(G, '%s.png' % filename, [0, 0, 1800, 1000], keep_aspect_ratio=True,vertex_size=20,
            vertex_frame_color='black',vertex_frame_width=1,layout=layout)

def GN(G,layout):
    m=G.number_of_edges()
    for turn in range(m):
        betweeness_dict=nx.edge_betweenness_centrality(G)
        betweeness_list=sorted(betweeness_dict.items(),key=lambda x:x[1],reverse=True)
        max_edge=betweeness_list[0][0]
        G.remove_edge(max_edge[0],max_edge[1])
        modularity=get_modularity_method(G)
        print ('turn=%d,newQ=%s'%(turn+1,modularity))
        save_graph(G,turn+1,modularity,layout)

def save_graph(G, q,modularity,layout):
    result = open('./%stxt/%s_result.txt' % (order, q), 'w')
    result.write('standard:\n' + str(A) + '\n')
    B = getNMI_B(G)
    result.write('self:\n' + str(B) + '\n')
    result.write('_' * 30 + 'compute NMI' + '_' * 30 + '\n')
    nmi = NMI(A, B)
    with open('./%stxt/NMI_MODULARITY.txt' % order, 'a') as op:
        op.write('%s_NMI:%s,' % (q, nmi))
        op.write('%s_modularity:%s\n' % (q, modularity))
    result.write('NMI:' + str(nmi) + '\n')

    nx.write_gml(G, "./%sgml/%s_result.gml" % (order, q))
    G = ig.Graph.Read_GML("./%sgml/%s_result.gml" % (order, q))
    result.write('_' * 25 + 'compute modularity' + '_' * 28 + '\n')
    result.write('modularity:' + str(modularity) + '\n')
    result.close()
    draw_graph(G, "./%spng/%s_result" % (order, q), layout)

def get_modularity_method(G):
    r= nx.number_connected_components(G)
    clustering = list(nx.connected_components(G))

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

def getNMI_B(G):
    components=nx.connected_component_subgraphs(G)

    tuple_list=[]
    component_count=1
    for component in components:
        for node in component:
            tuple_list.append((node,component_count))
        component_count+=1

    community_list=[]
    for item in sorted(tuple_list,key=lambda x:x[0]):
        community_list.append(item[1])
    return np.array(community_list)

def NMI(A,B):
    # len(A) should be equal to len(B)
    total = len(A)
    A_ids = set(A)
    B_ids = set(B)
    #Mutual information
    MI = 0
    eps = 1.4e-45
    for idA in A_ids:
        for idB in B_ids:
            idAOccur = np.where(A==idA)
            idBOccur = np.where(B==idB)
            idABOccur = np.intersect1d(idAOccur,idBOccur)
            px = 1.0*len(idAOccur[0])/total
            py = 1.0*len(idBOccur[0])/total
            pxy = 1.0*len(idABOccur)/total
            MI = MI + pxy*math.log(pxy/(px*py)+eps,2)
    # Normalized Mutual information
    Hx = 0
    for idA in A_ids:
        idAOccurCount = 1.0*len(np.where(A==idA)[0])
        Hx = Hx - (idAOccurCount/total)*math.log(idAOccurCount/total+eps,2)
    Hy = 0
    for idB in B_ids:
        idBOccurCount = 1.0*len(np.where(B==idB)[0])
        Hy = Hy - (idBOccurCount/total)*math.log(idBOccurCount/total+eps,2)
    MIhat = 2.0*MI/(Hx+Hy)
    return MIhat

if __name__=="__main__":
    G = ig.Graph.Read_GML('%s.gml' % gml_name)

    layout = G.layout_fruchterman_reingold()
    with open('layout%s.pkl' % order, 'w') as f:
        pickle.dump(layout, f)
    draw_graph(G, gml_name, layout)
    # layout = pickle.load(open('layout%s.pkl'%order))

    if os.path.exists('./%spng' % order):
        shutil.rmtree('./%spng' % order)  # 删除
    os.makedirs('./%spng' % order)
    if os.path.exists('./%sgml' % order):
        shutil.rmtree('./%sgml' % order)
    os.makedirs('./%sgml' % order)
    if os.path.exists('./%stxt' % order):
        shutil.rmtree('./%stxt' % order)
    os.makedirs('./%stxt' % order)

    G=nx.read_gml("%s.gml"%gml_name)
    GN(G,layout)
