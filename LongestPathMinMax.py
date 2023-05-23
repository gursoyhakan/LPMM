import copy
import random
import time
import math
import os
import numpy as np
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 19:05:46 2021

@author: hakan
"""

BIGNUM = 1000000000


def convert(print_path):
    converted_path = [1 for i in range(60)]
    for i in range(1, len(print_path)-1):
        j_day = (print_path[i]-2)//12
        j_action = print_path[i-1] % 12
        if j_action == 0:
            j_action = 12
        converted_path[j_day] = j_action
    return converted_path


def longest_path(max_w2):  # here we try to find the longest path, without passing the minmax limit
    weights = {}
    for j in nodes.keys():
        weights[j] = -1*BIGNUM
    weights[end] = 0
    new_max_w2 = -1
    parents = dict()
    node_keys = [i for i in nodes.keys()]
    for j in node_keys:
        parents[j] = -1
    node_keys.sort(reverse=True)
    for j in node_keys:
        if nodeweights[j] < max_w2:
            if nodeweights[j] > new_max_w2:
                new_max_w2 = nodeweights[j]
            for k in revadj[j]:
                if nodeweights[k] < max_w2:
                    if nodeweights[k] > new_max_w2:
                        new_max_w2 = nodeweights[k]
                    if weights[k] < weights[j]+edges[k, j]:
                        weights[k] = weights[j]+edges[k, j]
                        parents[k] = j
    return new_max_w2, parents, weights[start]

    
def first_pass(nodeweights):  # here we do the first pass traversal on the graph, to find the MINMAX value
    priority_q = []
    weights = {}
    for j in nodes.keys():
        weights[j] = BIGNUM
    weights[end] = 0
    priority_q.append(end)
    pivot = end
    visited = dict()
    for i in nodes.keys():
        visited[i] = 1
    visited[pivot] = 0
    visited[0] = 0
    is_it_done = 1
    while priority_q and is_it_done:
        pivot = 0
        for j in range(len(priority_q)):  # selects the minimum of the priority queue as pivot
            if weights[priority_q[j]] < weights[priority_q[pivot]]:
                pivot = j
        pivot = priority_q.pop(pivot)
        visited[pivot] = 0
        for j in revadj[pivot]:
            # passing through reverse adjacency list of the pivot, doing relaxation and pushing to priority queue
            if max(nodeweights[j], weights[pivot]) < weights[j]:
                weights[j] = max(nodeweights[j], weights[pivot])
                priority_q.append(j)
        if priority_q:
            k = 0
            for j in range(len(priority_q)):
                if weights[priority_q[k]] > weights[priority_q[j]]:
                    k = j
            priority_q[0], priority_q[k] = priority_q[k], priority_q[0]
        is_it_done = 0
        for t in nodes.keys():
                if visited[t]:
                    is_it_done = 1
    return weights[start]


def reading(FILENAME):#here we read the map from the file
    arr = np.loadtxt(FILENAME,delimiter=",")
    if FILENAME[3:7]=='road' or FILENAME[3:6]=='soc' :
        directed = 0
        ek = 0
    else:
        directed = 1
        ek = 1
    adjacency={}
    revadj={}
    nodenum=0
    nodeweights={}
    edgenum=0
    start=1
    end=30
    edges = {}
    nodes = {}
    labelnums={}
    for i in arr:
            edgenum += 1
            a=int(i[0])+ek
            b=int(i[1])+ek
            d=(i[2],i[3])
            edges[a,b]=d[0]
            nodeweights[a]=d[1]
            nodes.setdefault(a,1)
            nodes.setdefault(b,1)
            labelnums.setdefault(a,0)
            labelnums.setdefault(b,0)
            if directed:
                adjacency.setdefault(a,[]).append(b)
                revadj.setdefault(b,[]).append(a)
            else:
                adjacency.setdefault(a,[]).append(b)
                revadj.setdefault(b,[]).append(a)
                adjacency.setdefault(b,[]).append(a)
                revadj.setdefault(a,[]).append(b)
                nodeweights[b]=d[1]
                edges[b,a]=d[0]
                
    nodenum = len(nodes.keys())        
    return nodenum, edgenum,  edges, nodes, start, end, adjacency, labelnums, directed, revadj, nodeweights



# reading from the file
path = '/Users/hakangursoy/Desktop/doktora/yayınlar/osm/lpmm/'
files = os.listdir(path)
filelist=[]
for f in files:
	if f[-3:]=='txt' and f[0:3]=='BOA':
		filelist.append(f)
outfile = open(f"outfile.txt","w")
	
for fil in sorted(filelist):
    print(f"{fil} basladi\n")
    t1=time.time()
    nodenum, edgenum,  edges, nodes, start, end, adjacency, labelnums, directed, revadj, nodeweights= reading(fil)

    # below is the first pass to find MINMAX
    minW2 = first_pass(nodeweights)
    paths = list()
    max_w2 = BIGNUM
    while max_w2 >= minW2:
        max_w2, path, lp = longest_path(max_w2)
        #print(max_w2, lp, minW2)
        paths.append([lp, max_w2, path])
    #print(paths)
    if paths[-1][1] == 0:
        del(paths[-1])
    isunique = [1 for i in range(len(paths))]
    for i in range(len(paths)-1):
        if paths[i][0] == paths[i+1][0]:
            isunique[i] = 0
    t2 = time.time()
    f = open(f"result_{fil}", "w")
    strr = "Completion time: "
    strr += str(t2-t1)
    f.writelines(f"Completion time : {(t2-t1):.2f} seconds" )
    f.writelines("\n")
    t = -1
    printing_paths = {}
    printing_paths[0] = []
    print(f"{len(paths)}, tamamlandi")
    for i in paths:
        t += 1
        if isunique[t]:
            f.writelines(f"{i}\n")
            printing_paths[0].append((i[0], i[1], i))
    f.close()
    outfile.writelines(f"{fil} {(t2-t1):.2f} {nodenum} {edgenum}")

outfile.close()
