#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/9 上午12:18
# @Author  : Junnor.G
# @Site    : NJU
# @File    : my_fast_unfolding.py
# @Software: PyCharm

import networkx as nx
import os
import math

def load_data(path, split_char='\t'):

    nodes = []
    edges = []

    if os.path.exists(path) == False:
        print('file not exist of path: {}'.format(path))

    lines = open(path, 'r')

    for line in lines:
        edge = line.strip().split(split_char)

        u = int(edge[0]) - 1
        v = int(edge[1]) - 1

        if nodes.count(u) == 0:
            nodes.append(u)
        if nodes.count(v) == 1:
            nodes.append(v)
        edges.append((u, v, 1.))

    return nodes, edges


def load_graph(nodes, edges):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_weighted_edges_from(edges)
    # G[1][0]['weight'] += 3
    # print 'debug: {} {}'.format(G[1][0]['weight'], G[0][1]['weight'])
    # print 'debug: {}'.format(G[edges[0][0]][edges[0][1]])
    return G


def load_graph_from_path(path, split_char='\t'):
    nodes, edges = load_data(path, split_char)
    return load_graph(nodes, edges)

class FastUnfolding:

    def __init__(self, G):
        '''
        :param G: nx.Graph() 保证其中的节点是0 ~ G.number_of_nodes-1的简单图
        '''
        self.init_G = G.copy()
        self.G = G.copy()
        self.G_cluster = G.copy()  # 辅助处理社区之间连边的权值，G[u][v]表示社区u与社区v之间的权值
        self.sum_in = [0] * G.number_of_nodes()   # 当前社区内边连接数(sum_in[i]就是编号为i的社区中有多少条边)
        self.sum_tot = [0] * G.number_of_nodes()  # 当前社区总连接数(sum_tot[i]就是编号为i的社区中的点的总度数)
        self.cluster = [i for i in range(G.number_of_nodes())]  # 每个点所处的团的编号

        # index = -1
        # for i in range(150):
        #     if i % 10 == 0:
        #         index += 1
        #     self.cluster[i] = index
        self.n = G.number_of_nodes()
        self.m = 0.
        self.k = [0.] * self.n  # k[i] 代表与i相连的边的总权值
        self.update_k(G)

        self.update_sum(G)

        for edge in G.edges:
            self.m += G[edge[0]][edge[1]]['weight']

        self.cur_Q = self.modularity()
        self.can_update_node = [i for i in range(self.n)]  # 表示还可以更新为新社区的节点
        self.has_solve_node = [False] * self.n   # 表示已经处理过的点，辅助can_update_node

    def update_sum(self, G):  # according to cluster, update sum_in and sum_tot
        self.sum_in = [0] * self.n
        self.sum_tot = [0] * self.n
        for u in G.nodes():
            for v in G.neighbors(u):
                self.sum_tot[self.cluster[u]] += G[u][v]['weight']
                if self.cluster[u] == self.cluster[v]:
                    self.sum_in[self.cluster[u]] += G[u][v]['weight']*2
                    self.sum_tot[self.cluster[u]] += G[u][v]['weight']

    def modularity(self):
        Q = 0.
        self.update_cluster()
        self.update_sum(self.G_cluster)

        vis = [False] * self.n
        for u in G.nodes():
            if vis[self.cluster[u]] == True:
                continue
            vis[self.cluster[u]] = True
            # print 'here: cluster id is: {} \nsum_in: {} \nsum_tot: {}'.\
            #     format(self.cluster[u], self.sum_in[self.cluster[u]], self.sum_tot[self.cluster[u]])
            Q += self.sum_in[self.cluster[u]] / (2 * self.m)
            Q -= math.pow(self.sum_tot[self.cluster[u]] / (2 * self.m), 2)
        return Q

    # 根据算法本身，u一定是单独一个点作为一个社区的，下面的更新公式才有效
    def delta_modularity(self, u, c):  # 对于给定的G中将点u加入到社区c中
        if u == c:
            return -1.
        # print 'delta_modularity debug {}, {}, {}'.format(u, c, self.G_cluster[u][c]['weight'])
        first = (self.sum_in[c] + self.G_cluster[u][c]['weight'] * 2) / (2 * self.m) - \
                math.pow((self.sum_tot[c] + self.k[u]) / (2 * self.m), 2)

        second = self.sum_in[c] / (2*self.m) - \
                 math.pow(self.sum_tot[c] / (2 * self.m), 2) - \
                 math.pow(self.k[u] / (2 * self.m), 2)
        return first - second

    def update_modularity(self, u, c):  # 将点u加入到社区c中能使Q值增大, 那么做此处理，并更新相关的变量
        # print 'update_modularity: node', u, 'add to community ', c

        self.sum_in[c] += self.G_cluster[u][c]['weight'] * 2 + self.sum_in[u]

        self.sum_tot[c] += self.k[u]
        self.cluster[u] = c

        for v in self.G_cluster.neighbors(u):
            if v == u:
                self.G_cluster[c][c]['weight'] += self.G_cluster[u][v]['weight']
            else:
                if self.G_cluster.has_edge(c, v) == False:
                    self.G_cluster.add_edge(c, v, weight=self.G_cluster[u][v]['weight'])
                else:
                    # print u, c, v, self.G_cluster[c][v]['weight'], self.G_cluster[u][v]['weight']
                    self.G_cluster[c][v]['weight'] += self.G_cluster[u][v]['weight']

        self.G_cluster.remove_node(u)

        self.has_solve_node[u] = self.has_solve_node[c] = True
        # print 'before: ', self.sum_tot
        # self.update_sum(self.G_cluster)
        # print 'after : ', self.sum_tot

    '''
    一轮结束，将同一社区中的点缩成一个点，重构图跑下一轮
    '''
    def rebuild(self):
        self.G = self.G_cluster.copy()
        for u in self.G.nodes():
            self.has_solve_node[u] = False
            self.can_update_node.append(u)
        # print self.G_cluster.number_of_nodes()
        # print self.sum_in
        # print self.sum_tot
        self.update_sum(self.G)
        # print self.sum_in
        # print self.sum_tot
        self.update_k(self.G)
        # print 'debug: {}'.format(self.modularity())

        pass

    '''
    每一轮后更新cluster的k值，每个点的度数
    '''
    def update_k(self, G):
        for u in G.nodes():
            # self.G_cluster.add_edge(u, u, weight=0.)
            self.k[u] = 0.
            for v in G.neighbors(u):
                self.k[u] += G[u][v]['weight']
                if u == v:
                    self.k[u] += G[u][v]['weight']

    '''
    每一轮后更新cluster的id，类似并查集的思想，一直到它的父亲是自己为止，但我懒得写并查集了，多个循环解决算了
    '''
    def update_cluster(self):
        for i in range(self.n):
            cur = i
            while self.cluster[cur] != cur:
                cur = self.cluster[cur]
            self.cluster[i] = cur

    def run_one_round(self):
        flag = False
        for u in self.can_update_node:
            if self.has_solve_node[u]:
                continue
            optimal_delta = 0.
            optimal_cluster = -1
            for v in self.G.neighbors(u):
                if v == u:
                    continue
                delta = self.delta_modularity(u, self.cluster[v])
                if delta > optimal_delta:
                    optimal_delta = delta
                    optimal_cluster = self.cluster[v]

            if optimal_cluster != -1:
                self.cur_Q += optimal_delta
                self.update_modularity(u, optimal_cluster)
                # print 'after this update --> curQ: {}'.format(self.cur_Q)

                flag = True

        del_list = []
        for u in self.can_update_node:
            if self.has_solve_node[u] == True:
                del_list.append(u)
        for u in del_list:
            self.can_update_node.remove(u)
        return flag

    def running(self):
        rounds = 0
        print 'init Q is {}'.format(self.cur_Q)
        while self.run_one_round():
            rounds += 1
            print 'round {} start--------------------------------------------------'.format(rounds)
            self.update_cluster()

            print 'round {} finished --> cur Q is : {}'.format(rounds, self.cur_Q)
            print 'real modularity: {}'.format(self.modularity())
            self.rebuild()

            print 'after this round cluster id is : \n', self.cluster
            print 'round {} end--------------------------------------------------'.format(rounds)
            pass





if __name__ == '__main__':
    print 'start load data'
    G = load_graph_from_path('../data/artificial_data/30rings.txt')
    # G = load_graph_from_path('../data/ia-dbpedia-team-bi.edges', ' ')
    # G = load_graph_from_path('../data/karate/karate.txt')
    print 'finish load data'
    print 'number of nodes: {}'.format(G.number_of_nodes())
    print 'number of edges: {}'.format(G.number_of_edges())
    # print G.number_of_edges()
    # G.remove_node(1)
    # print G.number_of_edges()
    # print G.edges()

    fu = FastUnfolding(G)
    fu.running()


