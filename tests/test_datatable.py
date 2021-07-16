from datastack.datacolumn import DataColumn, are_equal
from datastack import DataTable 
from datastack.helper import _dicts_equal
import numpy as np 

import pytest

def test_init1():
    tbl = DataTable(a=(1,2,3), b=(4,4,6))
    assert _dicts_equal(tbl._data, {"a":np.array((1,2,3)), "b": np.array((4,4,6))})
    assert all(tbl._labels == np.array(("a","b")))


def test_init2():
    tbl = DataTable(a=(1,2,3), b=(4,"5",6))
    assert _dicts_equal(tbl._data, {"a":np.array((1,2,3)), "b": np.array(("4","5","6"))})
    assert all(tbl._labels == np.array(("a","b")))

def test_init3():
    tbl = DataTable._from_label_and_data(("a","b"),((1,2,3),(5,6,"7")))
    assert _dicts_equal(tbl._data, {"a":np.array((1,2,3)), "b": np.array(("5","6","7"))})
    assert all(tbl._labels == np.array(("a","b")))

def test_init4():
    tbl = DataTable()
    assert tbl._data == None
    assert tbl._labels == None

def test_init5():
    tbl = DataTable(a="1", b=2)
    #tbl = DataTable.from_dict({"a":1, "b":2})
    assert _dicts_equal(tbl._data, {"a":np.array(["1"]), "b":np.array((2))})
    assert all(tbl._labels == np.array(("a","b")))


def test_init5():
    tbl = DataTable(a="1", b=2)
    #tbl = DataTable.from_dict({"a":1, "b":2})
    assert _dicts_equal(tbl._data, {"a":np.array(["1"]), "b":np.array((2))})
    assert all(tbl._labels == np.array(("a","b")))


def test_len():
    tbl = DataTable(a=(1,2,3,4), b=(4,4,5,6))
    assert len(tbl) == 4

def test_get_column():
    tbl = DataTable(a=(1,2,4),b=(5,6,7))
    col = tbl.get_column("a")
    exp = DataColumn("a",(1,2,4))
    assert all(col == exp)

def test_get_row():
    tbl = DataTable(a=(1,2,3,4),b=(4,4,5,7))
    row = tbl.get_row(1)
    exp = DataTable(a=(2), b=(4))
    assert row == exp

    # only has 4 elements
    with pytest.raises(ValueError):
        tbl.get_row(4)

def test_order_by():
    tbl = (DataTable(a=(4,2,1,3), b=("a","b","c","a"), c=(10,9,8,7))
        ._order_by("b","a")
    )
    exp = DataTable(a=(3,4,2,1), b=("a","a","b","c"), c=(7,10,9,8))
    assert tbl == exp
    

def test_append_row():
    tbl = DataTable(a=(4,2,1,3), b=(1,2,3,4), c=(10,9,8,7))
    tbl.append_row(a=10, b=122.32323, c=14)
    exp = DataTable(a=(4,2,1,3,10), b=(1,2,3,4,122.32323), c=(10,9,8,7,14))
    assert tbl == exp
    
    tbl = DataTable(a=(4,2,1,3), b=(1,2,3,4), c=("10","9","8","7dfd"))
    tbl.append_row(a="10", b=122.32323, c=14)
    exp = DataTable(a=("4","2","1","3","10"), b=(1,2,3,4,122.32323), c=("10","9","8","7dfd","14"))
    assert tbl == exp