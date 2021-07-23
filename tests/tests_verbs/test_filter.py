from datastack import DataTable, DataColumn, col
import pytest 

def test_filter_equals():
    tbl = (DataTable(a=(1,2,3,4,5,6,4,7,8,4,1), b=list("abcdefghijk"))
        .filter(col("a").equals(4))
       )
    exp = DataTable(a=(4,4,4), b=list("dgj"))
    assert tbl == exp

def test_filter_larger_then():
    tbl = (DataTable(a=(1,2,3,4,5,6,4,7,8,4,1), b=list("abcdefghijk"))
           .filter(col("a").larger_then(4)))
    exp = DataTable(a=(5,6,7,8), b=list("efhi"))
    assert tbl == exp