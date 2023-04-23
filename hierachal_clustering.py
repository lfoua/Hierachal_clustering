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

# Perform agglomerative clustering
def agglomerative_clustering():
    
    data = pd.read_excel('Longotor1delta.xls')
    n_clusters = 1  # we wanna get to 1 cluster
    clusters_results = {}
    for i in ['sch9/wt','ras2/wt','tor1/wt' ]:
        data_col = data.loc[:, i]   
        curr_clusters = [(i,) for i in data_col] #every element is taken as a cluster at first
        clusters =[]
        while len(curr_clusters) > n_clusters:
            
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
            
            clusters.append(merge_indices)
            curr_clusters.append(merge_indices)
        clusters_results[i] = clusters
    return clusters_results
       

if __name__ == '__main__':
    print(agglomerative_clustering())
