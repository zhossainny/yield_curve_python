import numpy as np


def binary_search(arr, val):
    index = np.searchsorted(arr, val)
    if index < len(arr) and arr[index] == val:
        return index
    else:
        return -index-1
