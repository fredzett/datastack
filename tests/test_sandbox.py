from datastack.datacolumn import are_equal
import datastack as dt
from datastack import DataColumn, are_equal

from datastack.helper import _dicts_equal

import numpy as np


def test_dicts_equal():
    d1, d2 = dict(a=np.array(1), b=np.array(1)), dict(a=np.array(1), b=np.array(1))
    assert _dicts_equal(d1,d2)
    d1, d2 = dict(a=np.array((1,2,3)), b=np.array(1)), dict(a=np.array((1,2,3)), b=np.array(1))
    assert _dicts_equal(d1,d2)
    d1, d2 = dict(a=np.array((1,2,3)), b=list("abcd")), dict(a=np.array((1,2,3)), b=list("abcd"))
    assert _dicts_equal(d1,d2)

def test_from_dict():
    c = DataColumn.from_dict(h1=(1,2,3))
    assert are_equal(c, DataColumn("h1", (1,2,3)))

def test_to_dict():
    c = DataColumn("h1",(1,2,3))
    c = c.to_dict()
    assert _dicts_equal(c, {"h1":np.array((1,2,3))})


def test_equal_1():
    c = DataColumn("A", (1,2,4,5,6))
    out = c == c
    assert all(out == np.array((True, True, True, True, True)))

def test_notequal_1():
    c = DataColumn("A", (1,2,4,5,6))
    d = DataColumn("B", (2,1,2,3,2,3))
    out = c != d
    assert all(out == np.array((True, True, True, True, True)))

def test_equal_2():
    c = DataColumn("A", (1,2,4,5,6))
    out = c == 4
    assert all(out == np.array((False, False, True, False, False)))
    c = DataColumn("A", (1,1,1,1,1))
    out = c == 1 
    assert all(out == np.array((True, True, True, True, True)))

def test_notequal_2():
    c = DataColumn("A", (1,2,4,5,6))
    out = c != 4
    assert all(out == np.array((True, True, False, True, True)))
    c = DataColumn("A", (1,1,1,1,1))
    out = c != 1 
    assert all(out == np.array((False, False, False, False, False)))

def test_greaterthen_1():
    c = DataColumn("A", (1,2,4,5,6))
    out = c > c
    assert all(out == np.array((False, False,False,False,False)))

def test_greaterthen_2():
    c = DataColumn("A", (1,2,4,5,6))
    out = c > 4
    assert all(out == np.array((False, False, False, True, True)))
    c = DataColumn("A", (2,2,2,2,2))
    out = c > 1 
    assert all(out == np.array((True, True, True, True, True)))

def test_greaterequalthen_1():
    c = DataColumn("A", (1,2,4,5,6))
    out = c >= c
    assert all(out == np.array((True,True,True,True,True,)))

def test_greaterequalthen_2():
    c = DataColumn("A", (1,2,4,5,6))
    out = c >= 4
    assert all(out == np.array((False, False, True, True, True)))
    c = DataColumn("A", (2,2,2,2,2))
    out = c >= 1 
    assert all(out == np.array((True, True, True, True, True)))


def test_smallerthen_1():
    c   = DataColumn("A", (1,2,4,5,6))
    out = c < c
    assert all(out == np.array((False, False,False,False,False)))

def test_smallerthen_2():
    c   = DataColumn("A", (1,2,4,5,6))
    out = c < 3
    assert all(out == np.array((True, True,False,False,False)))

def test_smallerequalthen_1():
    c   = DataColumn("A", (1,2,4,5,6))
    out = c <= c
    assert all(out == np.array((True, True, True, True, True)))

def test_smallerequalthen_2():
    c   = DataColumn("A", (1,2,4,5,6))
    out = c <= 3
    assert all(out == np.array((True, True,False,False,False)))

def test_add_cols():
    c1 = DataColumn("A", (1,2,3))
    c2 = DataColumn("B", (3,4,5))
    out = c1 + c2 
    exp = DataColumn("A", (4,6,8))
    assert dt.are_equal(out, exp)

def test_add_col_int():
    c1 = DataColumn("A", (1,2,3))
    c2 = DataColumn("B", (3,4,5))
    out = c1 + 3 
    exp = DataColumn("A", (4,5,6))
    assert dt.are_equal(out, exp)

def test_add_int_col():
    c1 = DataColumn("A", (1,2,3))
    c2 = DataColumn("B", (3,4,5))
    out = 3 + c1
    exp = DataColumn("A", (4,5,6))
    assert dt.are_equal(out, exp)

def test_add_col_float():
    c1 = DataColumn("A", (1,2,3))
    c2 = DataColumn("B", (3,4,5))
    out = c1 + 3.123 
    exp = DataColumn("A", (4.123,5.123,6.123))
    assert dt.are_equal(out, exp)

def test_mul_cols():
    c1 = DataColumn("A", (1,2,3))
    c2 = DataColumn("B", (3,4,5))
    out = c1 * c2 
    exp = DataColumn("A", (3,8,15))
    assert dt.are_equal(out, exp)

def test_mul_col_int():
    c1 = DataColumn("A", (1,2,3))
    c2 = DataColumn("B", (3,4,5))
    out = c1 * 3 
    exp = DataColumn("A", (3,6,9))
    assert dt.are_equal(out, exp)

def test_mul_int_col():
    c1 = DataColumn("A", (1,2,3))
    c2 = DataColumn("B", (3,4,5))
    out = 3 * c1 * 1
    exp = DataColumn("A", (3,6,9))
    assert dt.are_equal(out, exp)


def test_div_cols():
    c1 = DataColumn("A", (1,2,3))
    c2 = DataColumn("B", (3,0.2,5))
    out = c1 / c2 
    exp = DataColumn("A", (1/3, 2/0.2, 3/5))
    assert dt.are_equal(out, exp)

def test_div_col_int():
    c1 = DataColumn("A", (1,2,3))
    out = c1 / 3 
    exp = DataColumn("A", (1/3, 2/3, 3/3))
    assert dt.are_equal(out, exp)
    out = c1 / 0
    exp = DataColumn("A", (np.inf, np.inf, np.inf))
    assert dt.are_equal(out, exp)

def test_div_int_col():
    c1 = DataColumn("A", (1.1,2,3))
    out = 3.1 / c1 
    exp = DataColumn("A", (3.1/1.1, 3.1/2, 3.1/3))
    print(exp)
    print(out)
    assert dt.are_equal(out, exp)

def test_sub_cols():
    c1 = DataColumn("A", (1,2,3))
    c2 = DataColumn("B", (3,0.2,5))
    out = c1 - c2 
    exp = DataColumn("A", (1-3, 2-0.2, 3-5))
    assert dt.are_equal(out, exp)

def test_sub_col_int():
    c1 = DataColumn("A", (1,2,3))
    out = c1 - 3 
    exp = DataColumn("A", (1-3, 2-3, 3-3))
    assert dt.are_equal(out, exp)
    

def test_sub_int_col():
    c1 = DataColumn("A", (1.1,2,3))
    out = 3.1 - c1 
    exp = DataColumn("A", (3.1-1.1, 3.1-2, 3.1-3))
    print(exp)
    print(out)
    assert dt.are_equal(out, exp)

def test_pow_cols():
    c1 = DataColumn("A", (1,2,3))
    c2 = DataColumn("B", (2,3,4))
    out = c1 ** c2 
    exp = DataColumn("A", (1, 8, 81))
    assert dt.are_equal(out, exp)

def test_pow_col_int():
    c1 = DataColumn("A", (1,2,3))
    out = c1 ** 3 
    exp = DataColumn("A", (1,8, 27))
    assert dt.are_equal(out, exp)
    

def test_pow_int_col():
    c1 = DataColumn("A", (1.1,2,3))
    out = 2.2 ** c1 
    exp = DataColumn("A", (2.2**1.1, 2.2**2, 2.2**3))
    assert dt.are_equal(out, exp)


def test_rename():
    c = DataColumn("OldName", list("abcd"))
    c = c.rename("NewName")
    exp = DataColumn("NewName", list("abcd"))
    assert are_equal(c, exp)
    c = DataColumn("OldName", (True, True, False))
    c = c.rename("NewName")
    exp = DataColumn("NewName", (True, True, False))
    assert are_equal(c, exp)