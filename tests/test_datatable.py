from datastack import DataTable 
import pytest
import numpy as np

### Test construction

#def dicts_equal(actual_dict, expected_dict):
#    return all(list((a[0] == b[0]) and all(a[1] == b[1]) for a,b in zip(actual_dict.items(), expected_dict.items())))

def test_init():
    tbl = DataTable(a=1, b=2)
    assert tbl._data == {"a":np.array([1]), "b":np.array([2])}

    tbl = DataTable(a=[1], b=[2])
    assert tbl._data == {"a":np.array([1]), "b":np.array([2])}

    tbl = DataTable(a=[1,2,3], b=[4,5,6])
    expected_dict = {"a":np.array([1,2,3]), "b":np.array([4,5,6])}
    actual_dict = tbl._data
    # Asserts!
    np.testing.assert_equal(actual_dict, expected_dict)

def test_from_dict():
    tbl = DataTable._from_dict({"a":np.array([1,2,3]), "b":np.array([4,5,6])})

    expected_dict = {"a":np.array([1,2,3]), "b":np.array([4,5,6])}
    # Asserts!
    np.testing.assert_equal(tbl._data, expected_dict)

def test_from_label_column():
    tbl = DataTable._from_label_column("a",[1,2,3])
    expected_dict = {"a": np.array([1,2,3])}
    # Asserts!
    np.testing.assert_equal(tbl._data, expected_dict)

def test_from_labels_columns():
    tbl = DataTable._from_labels_columns(["a", "b"],[[1,2,3], [4,5,6]])
    expected_dict = {"a":np.array([1,2,3]), "b":np.array([4,5,6])}
    # Asserts!
    np.testing.assert_equal(tbl._data, expected_dict)

### Test appending
def test_append_row():
    tbl = DataTable(a=[1,2,3],b=[4,5,6])
    tbl.append_rows([10, 13])

    tbl_expected = DataTable(a=[1,2,3,10],b=[4,5,6,13])
    assert tbl == tbl_expected


def test_append_columns():
    tbl = DataTable(a=[1,2,3],b=[4,5,6])
    tbl.append_columns(c=[1,2,3])

    tbl_expected = DataTable(a=[1,2,3],b=[4,5,6], c=[1,2,3])
    assert tbl == tbl_expected

    # Error: columns of different length
    with pytest.raises(ValueError):
        tbl = DataTable(a=[1,2,3],b=[4,5,6])
        tbl.append_columns(c=[1,2,3,4])

    # Error: column already exists
    with pytest.raises(ValueError):
        tbl = DataTable(a=[1,2,3],b=[4,5,6])
        tbl.append_columns(a=[1,2,3])

def test_is_equal_1d():
    
    tbl1 = DataTable(a=1,b=2)
    tbl2 = DataTable(a=1, b=2)
    assert tbl1 == tbl2

    tbl1 = DataTable(a="1",b=2)
    tbl2 = DataTable(a="1", b=2)
    assert tbl1 == tbl2
    
def test_is_equal_2d():
    
    tbl1 = DataTable(a=[1,2],b=[2,3])
    tbl2 = DataTable(a=[1,2], b=[2,3])
    assert tbl1 == tbl2

    tbl1 = DataTable(a=[1,2],b=[2,"3"])
    tbl2 = DataTable(a=[1,2], b=[2,"3"])
    assert tbl1 == tbl2

def test_drop_idx():
    tbl = DataTable(a=[1,2,3,4], b=[2,3,4,2], c=list("abcd"))
    tbl.drop(0)
    tbl_expected = DataTable(b=[2,3,4,2], c=list("abcd"))
    assert tbl == tbl_expected
    
    tbl = DataTable(a=[1,2,3,4], b=[2,3,4,2], c=list("abcd"))
    tbl.drop(1,2)
    tbl_expected = DataTable(a=[1,2,3,4])
    assert tbl == tbl_expected

def test_drop_bools():
    tbl = DataTable(a=[1,2,3,4], b=[2,3,4,2], c=list("abcd"))
    tbl.drop([False, True, True])
    tbl_expected = DataTable(a=[1,2,3,4])
    assert tbl == tbl_expected

    tbl = DataTable(a=[1,2,3,4], b=[2,3,4,2], c=list("abcd"))
    tbl.drop([True, True, True])
    tbl_expected = DataTable()
    assert tbl == tbl_expected

def test_select():
    tbl = DataTable(a=[1,2,3,4], b=[2,3,4,2], c=list("abcd"))
    tbl.select("a", "b")

    tbl_expected = DataTable(a=[1,2,3,4], b=[2,3,4,2])
    assert tbl == tbl_expected