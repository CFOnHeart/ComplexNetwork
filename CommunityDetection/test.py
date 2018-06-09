#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/6 下午9:45
# @Author  : Junnor.G
# @Site    : NJU
# @File    : test.py
# @Software: PyCharm


import matplotlib.pyplot as plt
import networkx as nx
from load_data import gml_data
path = '../data/karate/karate.gml'
nodes, edges = gml_data.load_gml_data(path)

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)


# 输出节点信息
print(G.nodes(data=True))

# 输出边信息
print(G.edges)

# 计算图或者网络的传递性
print(nx.transitivity(G))

# 节点个数
print(G.number_of_nodes())

# 边数
print(G.number_of_edges())

# 节点邻居个数
print(G.neighbors(1))

import igraph

g = igraph.Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])
igraph.plot(g, target="/tmp/igraph_demo.png")

