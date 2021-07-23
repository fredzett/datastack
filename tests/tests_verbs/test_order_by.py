from datastack import DataTable, DataColumn, label, col
import pytest 

import numpy as np

def test_one():
    tbl = (DataTable(a=(1,2,1,2,3,1), b=(4,5,6,3,2,1),c=(6,7,8,1,2,3))
          .order_by(label("b"), asc=[False])
          )
    exp = DataTable(a=(1,2,1,2,3,1), b=(6,5,4,3,2,1), c=(8,7,6,1,2,3))
    assert tbl == exp

def test_one_str():
    tbl = (DataTable(a=(1,2,1,2,3,1), b=(4,5,6,3,2,1),c=list("abcdef"))
          .order_by(label("b"))
          )
    exp = DataTable(a=(1,3,2,1,2,1), b=(1,2,3,4,5,6), c=list("fedabc"))
    assert tbl == exp

def test_two():
    tbl = (DataTable(b=(4,5,2,3,2,1),c=(6,7,8,1,2,3),a=(1,2,1,2,3,1))
          .order_by(label("b"), label("a"), label("c"), asc=[True, False, True])
          )
    exp = DataTable( b=(1,2,2,3,4,5), c=(3,2,8,1,6,7),a=(1,3,1,2,1,2))
    assert tbl == exp

def test_two_asc():
      data = {"col1": np.array((1, 2, 3, 4, 5, 4, 3, 2, 1)),
        "col2": np.array(list("abcdeabcd")),
        "col3": np.array((10, 11, 9, 8, 7, 2, 12, 100, 1))}

      tbl = (DataTable.from_dict(data)
            .order_by(label("col1"), label("col2"))
      )
      exp = DataTable.from_dict({'col1': np.array([1, 1, 2, 2, 3, 3, 4, 4, 5]),
                                    'col2': np.array(['a', 'd', 'b', 'c', 'b', 'c', 'a', 'd', 'e']),
                                    'col3': np.array([10, 1, 11, 100, 12, 9, 2, 8, 7])})
      assert tbl == exp

def test_two_asc_desc():
      data = {"col1": np.array((1, 2, 3, 4, 5, 4, 3, 2, 1)),
        "col2": np.array(list("abcdeabcd")),
        "col3": np.array((10, 11, 9, 8, 7, 2, 12, 100, 1))}

      tbl = (DataTable.from_dict(data)
            .order_by(label("col1"), label("col2"), asc=[True, False])
      )
      exp = DataTable.from_dict({'col1': np.array([1, 1, 2, 2, 3, 3, 4, 4, 5]),
 'col2': np.array(['d', 'a', 'c', 'b', 'c', 'b', 'd', 'a', 'e']),
 'col3': np.array([1, 10, 100, 11, 9, 12, 8, 2, 7])})
      assert tbl == exp


      