from datastack.datatable import DataTable
import pytest 

import datastack as dt 
import numpy as np

def test_desc():
    data = {"col1": np.array((1, 2, 3, 4, 5, 4, 3, 2, 1)),
        "col2": np.array(list("abcdeabcd")),
        "col3": np.array((10, 11, 9, 8, 7, 2, 12, 100, 1))}

    tbl = DataTable.from_dict(data)
    out = dt.desc(dt.label("col1"))._collect(tbl)
    order, idx = out
    assert order == False
    assert all(idx == np.array((True, False, False)))
    