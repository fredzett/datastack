from typing import Dict
import numpy as np
from numpy.lib.arraysetops import isin

# Checks if dicts in DataTable._data are equal
# needed because nested dicts containing different types (e.g. np.ndarray)
def _dicts_equal(a: Dict, b: Dict) -> bool:
    # Check if labels / columns are equal
    if a.keys() != b.keys():
        return False

    # Check if arrays are equal
    checks = []
    for arr1, arr2 in zip(a.values(), b.values()):
        if not isinstance(arr1, np.ndarray): arr1 = np.asarray(arr1)
        if not isinstance(arr2, np.ndarray): arr2 = np.asarray(arr2)
        #if arr1.dtype.type != arr2.dtype.type:
        #    return False
        if arr1.dtype.type is np.str_:
            checks.append(np.array_equal(arr1, arr2))
        else:
            
            checks.append(np.allclose(arr1, arr2, rtol=1e-08))
    if not all(checks):
        return False
    return True


def cols_are_equal(col1, col2):
    "Returns true"
    return all(col1 == col2)

