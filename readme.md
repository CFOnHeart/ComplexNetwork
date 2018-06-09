### 模块介绍

#### 1. load_data

加载数据模块，对于不同的数据文件，转化成自己需要的数据格式

#### 2. CommunityDetection

社团划分模块，不同的算法实现社团划分功能。

### 3.已经实现的算法

+ FastUnfolding: CommunityDetection/my_fast_unfolding.py

  根据Fast unfolding of communities in large networks (2008)论文中的 ring of 30 cliques ，实现了每个clique是个5个点的团作为测试数据的算法，效果和论文上一样，数据生成在data/artificial_data/30rings.txt中。
  数据格式为u\tv的形式。