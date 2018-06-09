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

order='08'

gml_name = './benchmark%s/network%s'%(order,order)

def FN(G,layout):
    VertexDendrograms = G.community_fastgreedy()  # 获取点系统树图
    clustering = VertexDendrograms.as_clustering()  # 转点聚类
    modulrity=clustering.modularity

    covers = clustering.as_cover()  # 转点覆盖
    n = len(covers)
    pal = ig.ClusterColoringPalette(n)
    i = 0
    for li in covers:
        for node in li:
            G.vs[node]['color'] = pal.get(i)
        i += 1
    ig.plot(G, '%s_new.png' % gml_name, [0, 0, 1800, 1000], keep_aspect_ratio=True, vertex_size=20,
            vertex_frame_color='black', vertex_frame_width=1, layout=layout)

    cover_list=[]
    for cover in covers:
        cover_list.append(cover)

    A = getNMI_A('./benchmark%s/community_network%s' % (order, order), '	')
    B=getNMI_B(cover_list,len(G.vs))
    nmi=NMI(A,B)

    with open('%sNMI_modularity.txt'%order,'w') as op:
        op.write('standard:\n')
        op.write(str(A)+'\n')
        op.write('self:\n')
        op.write(str(B) + '\n')
        op.write('NMI:%s,modularity:%s'%(nmi,modulrity))

def getNMI_A(filename,delimiter):
    community_list=[]
    reader = csv.reader(open('%s.txt'%filename), delimiter=delimiter)
    for line in reader:
        community_list.append(int(line[1]))
    return np.array(community_list)

def getNMI_B(cover_list,n):
    B=[0]*n
    count=1
    for cover in cover_list:
        for node in cover:
            B[node]=count
        count+=1
    return np.array(B)

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
    ig.plot(G, '%s.png' % gml_name, [0, 0, 1800, 1000], keep_aspect_ratio=True, vertex_size=20,
            vertex_frame_color='black', vertex_frame_width=1, layout=layout)
    FN(G,layout)
