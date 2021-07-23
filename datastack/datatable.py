from __future__ import annotations
from datastack.expressions import ColExpr, Expr, LabelExpr
from datastack import DataColumn 
from datastack.helper import _dicts_equal
import numpy as np
import pandas as pd # Work around!


from typing import Dict, OrderedDict, Tuple, Any, Collection, List, Type, Union
from numbers import Number 

class DataTable:
    def __init__(self, **labels_and_data: Dict[str, Tuple[Any]]):
        self._data, self._labels = self._check_and_process(**labels_and_data)
    
    
    def _check_and_process(self, **labels_and_data):
        '''Checks given input for DataTable and returns data and labels or raises Error'''
        d = labels_and_data 
        
        # d is empty
        if not bool(d): 
            return None, None
        
        # d is not empty
        out = {}  # Stores processed input
        labels = set()
        first = list(d.values())[0] # data of first column
        first = first if isinstance(first, Collection) and (not isinstance(first, str)) else [first]
        
        for label, column in d.items():
            # Check input validity
            if (not isinstance(column, Collection)) or isinstance(column, str):
                column = [column]
            if not len(column) == len(first):
                raise ValueError("Alle columns must have same length")
            if label in labels:
                raise ValueError("Column names must be unique")

            # Convert column to np.array if necessary
            if not isinstance(column, np.ndarray):
                column = np.array(column)

            out[label] = column

            # store label (all names must be unique)
            labels.add(label)
        
        labels = np.array(list(out.keys()))
        return out, labels


    def __len__(self):
        first = list(self._data.values())[0]
        return len(first)


    def __iter__(self):
        return TableIterator(self)

    def __repr__(self):
        return str(self._data)

    ##########################
    # from methods
    #########################
    @staticmethod
    def from_dict(d: Dict[str, Tuple[Any]]):
        return DataTable(**d)

    @staticmethod
    def _from_label_and_data(labels, columns):
       d = {label:data for label, data in zip(labels, columns)}
       return DataTable(**d)

    @staticmethod
    def _from_pandas(df: pd.DataFrame) -> DataTable:
        return DataTable.from_dict(df.to_dict('list'))    

    ##########################
    # to methods
    #########################
    def to_df(self):
        '''Converts DataTable into pandas dataframe'''
        d = self._data
        return pd.DataFrame(d)


    ##########################
    # Comparators
    #########################
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False 
        
        if _dicts_equal(self._data, other._data):
            if all(self._labels == other._labels):
                return True
        
        return False


    
    
    
    ##########################
    # Verbs
    #########################
    def filter(self, e: ColExpr) -> Self:
        '''Ich bin eine gute Beschreibung'''
        # Collect indices for which e is True
        idx = e._collect(self)
        if isinstance(idx, DataColumn): idx = idx._data
        # Return rows where idx == True
        for k,v in self._data.items():
            self._data[k] = v[idx]
        return self
    
    
    def select(self, *e: LabelExpr) -> Self:#Union[DataTable, DataColumn]:
        # Collect labels for which e is True
        exp = e[0]
        for es in e[1:]:
            exp |= es
        idx = exp._collect(self)
        #idx = e._collect(self)
        # Return labels where idx == True^
        labels = np.array(list(self._data.keys()))[idx]
        # TODO: clean up
        out = {}
        for label in labels:
            out[label] = self._data[label]
        return DataTable.from_dict(out)

    def mutate(self, **d: Dict[label: str, e: Union[ColExpr, Collection]]) -> Self:
        for label, exp in d.items():
            if isinstance(exp, Expr): 
                data = exp._collect(self)
            elif isinstance(exp, Collection):
                data = exp
            else:
                raise ValueError(f"Invalide datatype for mutation")
            
            self = self.append_column(**{label:data})
        return self
    

    def order_by(self, *e: LabelExpr, **kwargs) -> DataTable:
        
        # Check if sort order ('asc') was given
        if not "asc" in kwargs:
            asc = [True]
        else:
            asc = kwargs["asc"]
       
        # Unpack multiple expressions
        col_labels = [self._labels[expr._collect(self)][0] for expr in e]

        #  check and correct sort order list 
        n = len(col_labels)
        if len(asc) != n:
            if len(asc) == 1: 
                asc = asc * n
            else:
                raise ValueError(f"Sort order cannot contain {len(asc)} elements for {n} columns to sort.")
        
        # Reverse order for lexsort
        col_labels = col_labels[::-1]
        asc = asc[::-1]

        data = [self.get_column(label)._data for label in col_labels]
    
        idx = self._lexsort(data, asc)
        self._data = {k:v[idx] for k,v in self._data.items()}
        return self

    
    ##########################
    # Accessing
    #########################

    def get_column(self, s: str) -> DataColumn:
        if s not in self._labels: 
            raise ValueError(f"Column {s} not in DataTable ({self._labels})")
        return DataColumn(s, self._data[s])
    
    def get_row(self, i: int) -> DataTable:
        if (not isinstance(i, int)) or (i < 0): raise ValueError(f"Rows can only be accessed via a positive integer not via {type(i)}")
        if i >= len(self): raise ValueError(f"Cannot access row {i}. Table only has len of {len(self)}")

        data = list(self._data.items())
        out = {}
        for (label, values) in data:
            out[label] = values[i]
        
        return DataTable.from_dict(out)


    def __getitem__(self, idx):
        if isinstance(idx,str):
            return self.get_column(idx)
        else:
            raise NotImplementedError("TODO")


    ##########################
    # Append
    #########################
    def append_column(self, **d: Dict) -> Self:
        
        # Case 1: empty DataTable
        if not self._data: return DataTable.from_dict(d)

        # Case 2: non-empty DataTable
        new_data = dict(self._data) # Make copy of dict
        for label, data in d.items():
            #if label in self._labels:
            #    raise ValueError(f"Column '{label}' already exists!")
            new_data[label] = data
        self._data, self._labels = self._check_and_process(**new_data)
        return self


    def append_row(self, **d: Dict) -> Self:
        new_data = {}
        for l, value in d.items():
            column = np.hstack((self._data[l], np.array([value])))
            new_data[l] = column
        self._data, self._labels = self._check_and_process(**new_data) 
        return self

    def vstack(self, other) -> DataTable:
        if not isinstance(other, self.__class__): raise TypeError(f"Object of type {type(other)} cannot be stacked onto DataTable.")

        if sorted(self._labels) != sorted(other._labels): raise ValueError(f"Both DataTables must have the same column labels")
    
        out = DataTable()
        for label in self._labels:
            col1, col2 = self.get_column(label), other.get_column(label)
            col = col1.vstack(col2)
            out = out.append_column(**col.to_dict())
        return out

    def hstack(self, other) -> DataTable:
        if not isinstance(other, self.__class__): 
            raise TypeError(f"Object of type {type(other)} cannot be stacked onto DataTable.")

        for label in other._labels:
            col = other.get_column(label)
            self.append_column(**col.to_dict())
        return self
        #if set(self._labels).intersection(other._labels): ValueError(f"D")

    ##########################
    # Own methods
    #########################

    def _sum_by_col(self):
        out = {}
        for l in self._labels:
            out[l] = np.sum(self._data[l])
        return DataTable.from_dict(out)


    def _lexsort(self, arrs: List[np.ndarray], asc: List[bool]) -> np.ndarray[bool]:
        'Sort table by given columns'
        # See https://stackoverflow.com/questions/68486204/dict-sort-by-multiple-keys-descending-ascending
        def custom_lexsort(arrs, asc=True):
            """
            Lexsort a collection of arrays in ascending or descending order.

            Parameters
            ----------
            arrs : sequence[array-like]
                Sequence of arrays to sort.
            asc : array-like[bool]
                Sequence of True for ascending elements of `keys`,
                False for descending. Must broadcast to `(len(arrs),)`.
            """
            def make_key(a, asc):
                if np.issubdtype(a.dtype, np.number):
                    key = a
                else:
                    _, key = np.unique(a, return_inverse=True)
                if asc:
                    return key
                elif np.issubdtype(key.dtype, np.unsignedinteger):
                    return np.iinfo(key.dtype).max + 1 - key
                else:
                    return -key

            
            keys = [make_key(*x) for x in zip(arrs, asc)]
            return np.lexsort(keys) # lexsort requires reverse order

        #print(arrs, asc)
        return custom_lexsort(arrs, asc)


    def _contains(self, s: str) -> DataTable:
        out = {}
        for label, values in self._data.items():
            if s in label:
                out[label] = values
        return DataTable.from_dict(out)    



class TableIterator:
    'Iterator class used by DataTable'
    def __init__(self, tbl: DataTable):
        self._datatable = tbl
        self._idx = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        if self._idx < len(self._datatable):
            result = self._datatable.get_row(self._idx)
        else:
            raise StopIteration
        self._idx += 1
        return result 



