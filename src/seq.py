import time
import numpy as np
from node import Node
from setup import *

def generateSeqs(n):
    base = [0]*n
    seq = []
    n_bits(n, base, seq)
    return seq

# https://tutorialhorizon.com/algorithms/generate-all-n-bit-binary-strings/#google_vignette

def n_bits(n, arr_a, seq):
    if n <= 0:
        seq.append(list(arr_a))
    else:
        arr_a[n - 1] = 0
        n_bits(n - 1, arr_a, seq)
        arr_a[n - 1] = 1
        n_bits(n - 1, arr_a, seq)

def calcPhi(seq):
    n = len(seq)
    return (n-np.sum(seq))/n

# def sortCalcPhi(seq):
#     return -calcPhi(seq)

# s = sorted(generateSeq(n), key=sortCalcPhi)

def classifySeqs(seq_list):
    d = {}
    for s in seq_list:
        frac = calcPhi(s)
        if frac not in d:
            d[frac] = [s]
        else:
            temp = d[frac]
            temp.append(s)
            d[frac] = temp
    return d

def generateOrderedSeqs(n):
    s = generateSeqs(n)
    return classifySeqs(s)

