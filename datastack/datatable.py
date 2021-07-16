from __future__ import annotations
from datastack.expressions import ColExpr, LabelExpr
from datastack import DataColumn 
from datastack.helper import _dicts_equal
import numpy as np
from typing import Dict, Tuple, Any, Collection, List, Type, Union
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
    # Construction
    #########################
    @staticmethod
    def from_dict(d: Dict[str, Tuple[Any]]):
        return DataTable(**d)

    @staticmethod
    def _from_label_and_data(labels, columns):
       d = {label:data for label, data in zip(labels, columns)}
       return DataTable(**d)

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
    
    
    def select(self, e: LabelExpr) -> Self:#Union[DataTable, DataColumn]:
        # Collect labels for which e is True
        idx = e._collect(self)
        print(idx)
        # Return labels where idx == True^
        labels = np.array(list(self._data.keys()))[idx]
        # TODO: clean up
        out = {}
        for label in labels:
            out[label] = self._data[label]
        return DataTable.from_dict(out)

    def mutate(self, **d: Dict[label: str, e: ColExpr]) -> Self:
        label = list(d.keys())[0]
        exp = d.pop(label)
        data = exp._collect(self)
        self.append_column(label, data)
        return self

    def order_by(self, ) -> Self:
        raise NotImplementedError("TODO")

    #def order_by(self, *e: Expr) -> DataTable:
    #    col_labels = e(self)
    #    return self._order_by(*col_labels)
    
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
            return self.get_columm(idx)
        else:
            raise NotImplementedError("TODO")


    ##########################
    # Append
    #########################
    def append_column(self, label: str, data: Collection) -> DataTable:
        new_data = dict(self._data) # Make copy of dict
        if label in new_data.keys(): raise ValueError(f"Column '{label}' already exists!")
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

        # continue here!
        pass

    
    ##########################
    # Own methods
    #########################

    def _sum_by_col(self):
        out = {}
        for l in self._labels:
            out[l] = np.sum(self._data[l])
        return DataTable.from_dict(out)


    def _order_by(self, *labels: str) -> Self:
        'Sort table by given columns'
        
        data = [self.get_column(label)._data for label in reversed(labels)]
        idx = np.lexsort(data)
        for label, values in self._data.items():
            self._data[label] = values[idx]
        return self

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

