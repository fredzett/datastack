from datastack import DataTable, DataColumn, label, col
import pytest 

def test_select_contains():
    tbl = (DataTable(a=(1,2,3,4,5,6,4,7,8,4,1), b=list("abcdefghijk"))
            .select(label().contains("a"))
           )
    exp = DataTable(a=(1,2,3,4,5,6,4,7,8,4,1))
    assert tbl == exp

def test_mutate():
    tbl = (DataTable(a=(1,2,3,4,5,6,4,7,8,4,1), b=list("abcdefghijk"))
            .mutate(c=col("a") + 3, d=col("c") + -3)
            )
    exp = DataTable(a=(1,2,3,4,5,6,4,7,8,4,1),b=list("abcdefghijk"),c=(4,5,6,7,8,9,7,10,11,7,4), d=(1,2,3,4,5,6,4,7,8,4,1))
    assert tbl == exp

def test_mutate2():
    tbl = (DataTable(a=(1,2,3,4), b=list("abcd"))
            .mutate(c=(5,6,7,8))
            )
    exp = DataTable(a=(1,2,3,4), b=list("abcd"), c=(5,6,7,8))
    assert tbl == exp