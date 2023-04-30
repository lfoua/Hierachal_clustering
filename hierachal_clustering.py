#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 12:27:07 2023

@author: loufoua
"""
import math
import numpy as np
import pandas as pd

def distance_matrix(X):
    dist_matrix = {}             
    for i in range(len(X) - 1):
        arr = []
        for j in range(i+1, len(X)):
            dist = (min(X[i]) - min(X[j])) ** 2
            dist = math.sqrt(dist)
            arr.append(dist)
        dist_matrix[i]= arr
        del arr
    return dist_matrix

def find_min(matrix):
    min_value = 1
    key = 0
    min_index = 0
    for k, v in matrix.items():
      if min(v) < min_value:
        min_value = min(v)
        min_index = v.index(min_value)
        key = k
    return min_index,key

def get_candidate_genes():
    #import the textfile and put it in a list
    lista=pd.read_csv('Candidate_genes.txt',sep='\n',header=None)[0].tolist()

    #remove the the 2 backslach 
    #for ind,elt in enumerate (lista):
        #elt= elt[:len(elt)-1]
        #lista[ind]=elt
    #print(len(lista))

    #delete any non candidate gene
    data = pd.read_excel('Longotor1delta.xls')
    data_col = data["Public ID"].tolist()
    #print(len(data_col))
    for i in range(len(data_col)):
        if data_col[i] not in lista:
            data = data.drop(labels=[i], axis=0)
    return data

#while there are srill elements to cluster
def stop_clustering(x, y):
    return any((True for a in x if a in y))
# Perform agglomerative clustering
def agglomerative_clustering():
    
    data = get_candidate_genes()
    clusters_results = {}
    
    for i in ['sch9/wt_normalized','ras2/wt_normalized','tor1/wt_normalized']:
        data_col = data.loc[:, i] 
        curr_clusters = [(i,) for i in data_col] #every element is taken as a cluster at first
        clusters = [(i,) for i in data_col]
        while len(curr_clusters) > 6:
            
            dist_matrix = distance_matrix(curr_clusters)
            min_index, key = find_min(dist_matrix)
            row= key
            col= min_index+row+1 if min_index+row+1 < len(curr_clusters) else 0
            row_tup = list(curr_clusters[row])
            col_tup = list(curr_clusters[col])
            row_tup.extend(col_tup)
            merge_indices = tuple(row_tup)
            
            del curr_clusters[col]
            del curr_clusters[row]
            
            curr_clusters.append(merge_indices)
        clusters_results[i] = curr_clusters
        
    return clusters_results
"""def longevity_ids():
    for k, v in clusters_results.items():
        """
#go through longevity_genes, get their sch9/wt, and put them
#in a list and use hte list down here for the comparison
def longevity_genes():
    clusters_results = agglomerative_clustering()
    longevity_genes=pd.read_csv('Longevity_genes.txt',sep='\n',header=None)[0].tolist()
    data = pd.read_excel('Longotor1delta.xls')
    for i in ['sch9/wt','ras2/wt','tor1/wt']:
                   arr=[]
                   for j in clusters_results.values():
                       arra=[]
                       for k in j:
                          for l in k:
                              #l = "%.4f" % l
                              #print(l)
                              try:
                                  df=data.query(i==l)['Public ID']
                                  print(df) 
                                  arra.append(df)
                              except:
                                  pass 
                       arr.append(arra)
                   clusters_results[i]=arr
    
    longevity_candidates = []
    for i in clusters_results.values():
        if any((True for a in longevity_genes if a in i)):
            longevity_candidates.append(i)
    return longevity_candidates, clusters_results


#print(longevity_genes())
if __name__ == '__main__':
    #print(agglomerative_clustering())
    print(longevity_genes())
