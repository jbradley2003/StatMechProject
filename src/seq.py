import numpy as np
from setup import *

def generateSeqs(n):
    """
    Returns list containing all possible sequence lists of an input size.
    
    :param n: Residue count (integer)
    """
    base = [0]*n
    seq = []
    n_bits(n, base, seq)
    return seq

# Function is from https://tutorialhorizon.com/algorithms/generate-all-n-bit-binary-strings/#google_vignette
def n_bits(n, arr_a, seq_list):
    """
    Generates all possible sequence lists of an input size and appends them to input list.
    
    :param n: Residue count (integer)
    :param arr_a: Placeholder list for recursive function (list)
    :param seq_list: List containing all sequence lists (list of lists of integers)
    """
    if n <= 0:
        seq_list.append(list(arr_a))
    else:
        arr_a[n - 1] = 0
        n_bits(n - 1, arr_a, seq_list)
        arr_a[n - 1] = 1
        n_bits(n - 1, arr_a, seq_list)

def calcPhi(seq):
    """
    Calculates the fraction of H-H contacts in an input sequence of residues.
    
    :param seq: Sequence list (list of integers)
    """
    n = len(seq)
    return (n-np.sum(seq))/n

def sortCalcPhi(seq):
    """
    Sorting function for sequences with most to least H-H contacts.
    
    :param seq: Sequence list (list of integers)
    """
    return -calcPhi(seq)

def classifySeqs(seq_list):
    """
    Returns a dictionary with sequences grouped by calcPhi result.
    
    :param seq_list: List containing all sequence lists (list of lists of integers)
    """
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

def generateSeqDict(n):
    """
    Returns a dictionary with sequences of input size grouped by calcPhi result.
    
    :param n: Residue count (integer)
    """
    return classifySeqs(generateSeqs(n))