#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/6 下午12:06
# @Author  : Junnor.G
# @Site    : NJU
# @File    : spectral_analysis.py
# @Software: PyCharm

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from load_data import gml_data

nodes, edges = gml_data.load_gml_data('../data/karate/karate.gml')
print(len(nodes), len(edges))

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

print(G.edges)


