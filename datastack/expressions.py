from __future__ import annotations
from datastack.datacolumn import DataColumn
from typing import List, Union, Any, Callable

from abc import ABC

import numpy as np
import inspect
#############################
# Meta class for expressions
#############################


class Expr(ABC):
    'Parent class for expression subclasses'
    def __init__(self):
        self.f = None
        
    @staticmethod
    def from_expr(e: Expr) -> Expr:
        expr = Expr.__new__(Expr)
        expr._expr = e 
        return expr
    
    @staticmethod
    def from_func(f: Callable) -> Expr:
        expr = Expr.__new__(Expr)
        expr.f = f
        return expr
    
    def __and__(self, other: Expr) -> Expr:
        f = lambda x: self._collect(x) & other._collect(x)
        return Expr.from_func(f)
    
    
    def __or__(self, other: Expr) -> Expr:
        f = lambda x: self._collect(x) | other._collect(x)
        return Expr.from_func(f)
    
    def AND(self, other) -> Expr:
        return self & other
    
    def OR(self, other) -> Expr:
        return self | other

    def __add__(self, other):
        if isinstance(other, Expr):
            f = lambda x: self._collect(x) + other._collect(x)
        else:
            f = lambda x: self._collect(x) + other
        return Expr.from_func(f)

    __radd__ = __add__

    def __mul__(self, other):
        if isinstance(other, Expr):
            f = lambda x: self._collect(x) * other._collect(x)
        else:
            f = lambda x: self._collect(x) * other
        return Expr.from_func(f)

    def __rmul__(self, other):
        return other.__mul__(self)

    def add(self, other):
        return self + other
    
    def mul(self, other):
        return self * other

    def _collect(self, x: Any) -> np.ndarray[bool]:
        '''Executes combined expressions for data x and returns array of bools
        indicating for which x expression is True/False'''
        def _unpack(e: Expr) -> List[Callable]:
            has_expr = True
            expr = e
            es = [expr]
            while has_expr:
                if hasattr(expr, "_expr"): 
                    expr = expr._expr
                    es.append(expr)
                else:
                    return es
            return es
        
        es = _unpack(self)
        args = x
        for e in reversed(es):
            if hasattr(e, "f"):
                args = e.f(args)
        if isinstance(args, DataColumn): args = args._data
        return args
    


#############################
# ColumnExpressions:
#############################

def wrap_colexpr(e: ColExpr) -> ColExpr:
    'Wraps multiple expressions piped together and always returns a new expression holding info of previous expressions'
    return ColExpr.from_expr(e)

class ColExpr(Expr):
    'Expressions for operations on DataColumns'        
    @staticmethod
    def from_expr(e: ColExpr) -> ColExpr:
        expr = ColExpr.__new__(ColExpr)
        expr._expr = e 
        return expr
    
    def col(self, s: str) -> ColExpr:
        f = lambda x: x.get_column(s)
        self.f = f
        return wrap_colexpr(self)

    def equals(self, el: Any) -> ColExpr:
        f = lambda x: x == el
        self.f = f
        return wrap_colexpr(self)

    def larger_then(self, el: Any) -> ColExpr:
        f = lambda x: x > el
        self.f = f 
        return wrap_colexpr(self)

    def __le__(self, other):
        raise NotImplementedError("To Come")

        
def col(s: str) -> ColExpr:
    'Syntactic shortcut for ColExpr().col(s)'
    return ColExpr().col(s)


#############################
# LabelExpressions:
#############################

def wrap_labelexpr(e: LabelExpr) -> LabelExpr:
    'Wraps multiple expressions piped together and always returns a new expression holding info of previous expressions'
    return LabelExpr.from_expr(e)

class LabelExpr(Expr):
    'Expressions for operations on DataTable labels'
    @staticmethod
    def from_expr(e: LabelExpr) -> LabelExpr:
        expr = LabelExpr.__new__(LabelExpr)
        expr._expr = e 
        return expr
    
    def label(self, s: str = None) -> LabelExpr:
        # Case 1: return all labels
        if not s:
            f = lambda x: np.array(list(x._data.keys()))
        
        # Case 2: return specified labels
        else:
            if isinstance(s, str): s = [s]
            f = lambda x: np.array([True if el in s else False for el in list(x._data.keys()) ])
                
        self.f = f
        return wrap_labelexpr(self)
    
    def contains(self, s: str) -> LabelExpr:
        f = lambda x: np.array([True if s in el else False for el in x])
        self.f = f
        return wrap_labelexpr(self)

    def replace(self, srch, rplc) -> LabelExpr:
        f = lambda x: np.array([el.replace(srch, rplc) for el in x])
        self.f = f 
        return wrap_labelexpr(self)

    def desc(self, l: LabelExpr) -> LabelExpr:
        f = lambda x: (False, l._collect(x))
        self.f = f
        return wrap_labelexpr(self)

def label(s: str = None) -> LabelExpr:
    return LabelExpr().label(s)

def desc(l: LabelExpr) -> LabelExpr:
    return LabelExpr().desc(l)

