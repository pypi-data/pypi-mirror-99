#!encoding=utf-8

import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine

'''
# 计算欧几里德距离：
'''
def euclidean(p, q):
    '''
    计算向量间欧几里得距离，并归一化
    向量不等长，则按照短的那个尺寸计算
    '''
    short_lenth = min(len(p), len(q))
    e = sum([(p[i] - q[i]) ** 2 for i in range(short_lenth)])
    return 1 / (1 + e ** .5)

def pearson(*args):
    A = np.array(args)
    dist_out = 1-pairwise_distances(A, metric="cosine")
    return dist_out

def manhattan(p, q):
    '''
    #计算曼哈顿距离：
    '''
    short_lenth = min(len(p), len(q))
    n = short_lenth
    vals = range(n)
    distance = sum(abs(p[i] - q[i]) for i in vals)
    return distance

def jaccrad(source, target):
    '''
    jaccrad系数， 参数为0，1二元值时的相似性计算
    '''
    up = set(source) & set(target)
    down = (set(source) | set(target)) - up
    return float(len(up) / len(down))

if __name__ == "__main__":
    a,b,c = [1,2,3,4,5,6], [1,2,3,4,5,7], [4,5,6,7,8,9]
    print(jaccrad(a,b))
    print(pearson(a,b,c))
    print(cosine_similarity([a],[b]))
    print(euclidean(a,b))
    print(manhattan(a,b))


