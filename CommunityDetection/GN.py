#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/6 下午3:12
# @Author  : Junnor.G
# @Site    : NJU
# @File    : GN.py
# @Software: PyCharm

import networkx as nx
from networkx import linalg
from load_data import gml_data
import numpy as np

'''
cal modualarity of G
G: networkx.Graph()
spectrals: dict{node_id1: spectral_id1, ...}
且保证spectrals中的spectral id 都是[1, n]的整数
n: count of spectral
'''
def modualarity(G, spectrals, n):
    unit_weight = 1.0 / len(G.edges)
    e = np.zeros(shape=(n, n))
    for edge in G.edges:
        spectral_id1 = spectrals[edge[0]] - 1
        spectral_id2 = spectrals[edge[1]] - 1
        if spectral_id1 != spectral_id2:
            e[spectral_id1, spectral_id2] += unit_weight
            e[spectral_id2, spectral_id1] += unit_weight
        else:
            e[spectral_id1, spectral_id1] += unit_weight

    Q = 0.
    for i in range(n):
        Q += e[i, i]
        ai = sum(e[i, :])
        Q -= ai*ai

    return Q

'''
1. bfs: calculate points' weight
2. calculate edges betweenness
3. find the edge e of max betweenness
4. remove e
'''
def remove_max_betweenness_edge(G):
    # 1. bfs
    weights = [0]

    pass

def bfs(G, v, weight):
    pass

if __name__ == '__main__':
    nodes, edges = gml_data.load_gml_data('../data/karate/karate.gml')
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    spectrals_1 = [1,2,4,5,6,7,8,11,12,13,14,17,18,20,22]

    spectrals = {}
    for v in nodes:
        if spectrals_1.count(v) > 0:
            spectrals[v] = 0
        else:
            spectrals[v] = 1

    n = 2
    #1 1 2 1 3 3 3 1 4 5 3 1 1 1 4 4 3 1 4 1 4 1 4 4 2 2 4 2 2 4 4 2 4 4
    spectrals = {1: 1, 2: 1, 3: 2, 4: 1, 5: 3, 6: 3, 7: 3, 8: 1, 9: 4, 10: 5,
                 11: 3, 12: 1, 13: 1, 14: 1, 15: 4, 16: 4, 17: 3, 18: 1, 19: 4, 20: 1,
                 21: 4, 22: 1, 23: 4, 24: 4, 25: 2, 26: 2, 27: 4, 28: 2, 29: 2, 30: 4,
                 31: 4, 32: 2, 33: 4, 34: 4}
    Q = modualarity(G, spectrals, 5)
    print (Q)

    # 1. bfs
    weights = [0] * (1 + max(G.nodes))
    distances = [-1] * (1 + max(G.nodes))
    # print(weights)
    for v in G.nodes:
        if weights[v] == 0:
            weights[v] = 1
            distances[v] = 0
            # bfs(v, G, weights)
            que = [v]
            head = 0 ; tail = 1
            while head < tail:
                u = que[head]
                head += 1
                for t in G[u].keys():
                    if distances[t] == -1 or distances[t] == distances[u] + 1:
                        if distances[t] == -1:
                            distances[t] = distances[u] + 1
                            que.append(t)
                            tail += 1
                        weights[t] += weights[v]

    print(weights)
    pass
