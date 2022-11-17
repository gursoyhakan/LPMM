import copy
import time
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 19:05:46 2021

@author: hakan
"""
FILENAME="bigmapLongestPath.txt"
BIGNUM=1000000000


def LP(MaxW2): #here we try to find the longest path, without passing the minmax limit
        weights={}
        for j in range(1,nodenum+1):
            weights[j]=-1*BIGNUM
        weights[end]=0
        newMaxW2=-1
        parents=[-1 for i in range(nodenum+1)]
        for j in range(nodenum,0,-1):
          if nodeweights[j]<maxW2:
            if nodeweights[j]>newMaxW2:
                newMaxW2=nodeweights[j]
            for k in revadj[j]:
              if nodeweights[k]<maxW2:  
                if nodeweights[k]>newMaxW2:
                    newMaxW2=nodeweights[k]
                if weights[k]<weights[j]+edges[k,j]:
                    weights[k]=weights[j]+edges[k,j]
                    parents[k]=j
        return newMaxW2, parents, weights[start]
    
def firstpass(): #here we do the first pass traversal on the graph, to find the MINMAX value
        priorityQ=[]
        weights={}
        for j in range(1,nodenum+1):
            weights[j]=BIGNUM
        weights[end]=0
        priorityQ.append(end)
        pivot=end
        visited=[1 for i in range(nodenum+1)]
        visited[pivot]=0
        visited[0]=0
        isitdone=1
        while (priorityQ and isitdone):
            pivot=0
            for j in range(len(priorityQ)):# selects the minimum of the priority queue as pivot
                if weights[priorityQ[j]]<weights[priorityQ[pivot]]:
                    pivot=j
            pivot=priorityQ.pop(pivot)
            visited[pivot]=0
            for j in revadj[pivot]:#passing through reverse adjacency list of the pivot, doing relaxation and pushing to priority queue
                if max(nodeweights[j],weights[pivot])<weights[j]:
                    weights[j]=max(nodeweights[j],weights[pivot])
                    priorityQ.append(j)
            if (priorityQ):
                k=0
                for j in range(len(priorityQ)):
                    if weights[priorityQ[k]]>weights[priorityQ[j]]:
                        k=j
                priorityQ[0],priorityQ[k]=priorityQ[k],priorityQ[0]
            isitdone=0
            for t in range(nodenum+1):
                if visited[t]:
                    isitdone=1
        return weights[start]            


def reading():#here we read the map from the file
    f=open(FILENAME)
    str1=f.readline()
    str2=str1.split(",")
    adjacency={}
    revadj={}
    nodenum=eval(str2[0])
    edgenum=eval(str2[1])
    start=eval(str2[2])
    end=eval(str2[3])
    edges={}
    labelnums={}
    nodeweights={}
    for i in range(nodenum):
        adjacency[i+1]=[]
        revadj[i+1]=[]
        labelnums[i+1]=0
        str1=f.readline()
        str2=str1.split(",")
        a=eval(str2[0])
        b=eval(str2[1])
        nodeweights[a]=b
    for i in range(edgenum):
        str1=f.readline()
        str2=str1.split(",")
        a=eval(str2[0])
        b=eval(str2[1])
        c=eval(str2[2])
        edges[a,b]=-1*c
        adjacency[a].append(b)
        revadj[b].append(a)
            
    f.close()
    return nodenum, edgenum,  edges, start,end, adjacency,labelnums, revadj, nodeweights

#reading from the file
t1=time.time()
nodenum, edgenum,  edges, start, end, adjacency, labelnums, revadj, nodeweights= reading()
#above are the global variables

#below is the first pass to find MINMAX
minW2=firstpass()

paths=[]
maxW2=BIGNUM
while maxW2>=minW2:
    maxW2,path,lp= LP(maxW2)
    paths.append([lp,maxW2,path])
if paths[-1][1]==0:
        del(paths[-1])
isunique=[1 for i in range(len(paths))]
for i in range(len(paths)-1):
    if paths[i][0]==paths[i+1][0]:
        isunique[i]=0

t2=time.time()
print(t1)
print(t2)
t2-=t1
f=open("LongestPathmmout.txt","w")
strr="Completion time: "
strr+=str(t2-t1)
f.writelines(f"Completion time : {t2:.2f} seconds" )
f.writelines("\n")
t=-1
for i in paths:
  t+=1
  if isunique[t]:  
    strr="[ Total length of the path (First Criteria) : "
    strr+=str(i[0])
    strr+="- MinMax of path (Second criteria) : "
    strr+=str(i[1])
    strr+=" *** Nodes in the path=> "
    k=i[2][start]
    strr+=str(start)
    while k!=-1:
        strr+="->"+str(k)
        k=i[2][k]
    strr+="]"    
    f.writelines(strr)
    f.writelines("\n")
f.close()
