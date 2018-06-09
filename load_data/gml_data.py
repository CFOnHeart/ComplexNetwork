#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/6 下午2:43
# @Author  : Junnor.G
# @Site    : NJU
# @File    : gml_data.py
# @Software: PyCharm

import os

'''
以karate.gml 的格式读入数据的
  node
  [
    id 30
  ]
  edge
  [
    source 6
    target 1
  ]
'''

def load_gml_data(path):
    if not os.path.exists(path):
        print('file path {} not exists'.format(path))
        return

    try:
        fr = open(path, 'r')
        lines = fr.readlines()
        nodes = []
        edges = []
        for i in range(len(lines)):
            v = lines[i].strip()
            if v == 'node':
                tmp = lines[i+2].strip().split(' ')
                nodes.append(int(tmp[1]))
                i += 3
            if v == 'edge':
                tmpu = lines[i+2].strip().split(' ')
                tmpv = lines[i+3].strip().split(' ')
                edges.append((int(tmpu[1]), int(tmpv[1])))
        return nodes, edges
    except:
        print('file path {} not exists or this is not a valid file'.format(path))
        return


'''
以karate.gml 的格式读入数据的
  node
  [
    id 30
  ]
  edge
  [
    source 6
    target 1
  ]
转化为
u\tv
的文件格式
'''
def gml_to_txt(path):
    nodes, edges = load_gml_data(path)
    fw = open(path[:-3]+'txt', 'w')
    for edge in edges:
        fw.write(str(edge[0])+'\t'+str(edge[1])+'\n')


if __name__ == '__main__':
    gml_to_txt('../data/karate/karate.gml')
