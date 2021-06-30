from __future__ import annotations 
#import collections
import numpy as np 
from typing import Collection, Dict, List, Union, Tuple

def _len_first(d: Dict) -> np.ndarray:
    first = list(d.values())[0]
    if isinstance(first, (int, float, bool, str)): 
        return 1
    else:
        return len(first)

def _process_input(col_data):
    
    out = {} # Stores processed input
    labels = set()
    len_first = _len_first(col_data)
    for label, column in col_data.items():
        
        # Check input validity
        if (not isinstance(column, Collection)) or isinstance(column, str): column = [column]
        if not len(column) == len_first: raise ValueError("Alle columns must have same length")
        if label in labels: raise ValueError("Column names must be unique")

        # Convert column to np.array if necessary
        if not isinstance(column, np.ndarray): column = np.array(column)

        out[label] = column

        # store label (all names must be unique)
        labels.add(label)
    return out

class DataTable:
    def __init__(self, **col_data):

        if not col_data:
            self._empty()
        else:
            self._data = _process_input(col_data)  # holds data dict
            self._labels = np.array(list(self._data.keys())) # stores order of columns (first elment = first column)
            self.shape = (_len_first(self._data), len(self._labels))
                

    def _empty(self):
        self._data = {}
        self._labels = []
        self.shape =  ()

    # Should be used internally to update data in self!!
    def _update_data(self, d: Dict) -> self:
        if not d: 
            self._empty()
        else:
            self._data = _process_input(d)
            self._labels = np.array(list(self._data.keys()))
            self.shape = (_len_first(self._data), len(self._labels))

    ##########################
    ##### Construction
    #########################
    @classmethod
    def _from_dict(cls, d: Dict) -> DataTable:
        return cls(**d)
    
    @classmethod
    def _from_labels_columns(cls, labels, columns):
        if len(labels) != len(columns): raise ValueError("Labels and columns must be of same size")
        
        out = {}
        for l, c in zip(labels, columns):
            out[l] = c if isinstance(c, np.ndarray) else np.array(c)
        return cls._from_dict(out)
    
    @classmethod
    def _from_label_column(cls, label, column):
        return cls._from_labels_columns([label], [column])
    
    
    ##########################
    ##### Append data
    #########################
    def append_rows(self, row: List) -> DataTable:
        if len(row) != len(self._labels): raise ValueError(f"Row has size {len(row)}, but DataTable has {len(self._labels)} columns.")
        out = {}
        for (l, v), el in zip(self._data.items(), row):
            out[l] = np.append(self._data[l], el)
        
        self._update_data(out)
        return self
    
    def append_columns(self, **col_data) -> DataTable:

        out = self._data
        for label, column in col_data.items():
            if label in out.keys(): raise ValueError("Column already exists")
            out[label] = column
        self._update_data(out)
        return self

    #########################
    ##### Mutations
    #########################

    def _drop_by_idxs(self, *idxs: Tuple[int]) -> DataTable:
        
        # no input provided
        if not idxs: return self
        # Wrong input provided
        if not (type(idxs[0]) == int): raise ValueError(f"Column cannot be dropped using {idxs[0]}")
        
        # Check if provided indices exist
        idxs_true = range(len(self._labels))
        if not all(True if idx in idxs_true  else False for idx in idxs): raise ValueError(f"Indices {idxs} do not match existing indices {idxs_true}")
        
        out = {}
        for i, label in enumerate(self._labels):
            if not i in idxs:
                out[label] = self._data[label]
        self._update_data(out)
        return self

    def _drop_by_bools(self, idxs: List[bool]) -> DataTable:
        
        if not isinstance(idxs, list): raise ValueError("Columns to be dropped must be indicated via name, index or true/false")
        if not len(idxs) == len(self._labels): raise ValueError(f"Length of list of true/false {len(idxs)} does not match number of columns {len(self._labels)}")

        out = {}
        use_cols = np.array(self._labels)[~np.array(idxs)] # Drop if idxs is True
        for label in use_cols:
            out[label] = self._data[label]
        self._update_data(out)
        return self

    def drop(self, *idx: Union[Tuple[int], List[bool]]) -> DataTable:
        if type(idx[0]) == int:
           return self._drop_by_idxs(*idx)
        if isinstance(idx[0],List) & (type(idx[0][0]) == bool):
            return self._drop_by_bools(idx[0])
        raise ValueError("Something went wrong. Could not drop columns")

    #########################
    ##### Operations
    #########################
    def __add__(self, other):
        if isinstance(other, (float, int)):
            for label, _ in self._data.items():
                self._data[label] += other
            return DataTable._from_dict(self._data)
        else:
            NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, (float, int)):
            for label, _ in self._data.items():
                self._data[label] -= other
            return DataTable._from_dict(self._data)
        else:
            raise NotImplementedError
    
    def __mul__(self, other):
        if isinstance(other, (float, int)):
            for label, _ in self._data.items():
                self._data[label] *= other
            return DataTable._from_dict(self._data)

    def __eq__(self, other):

        if isinstance(other, self.__class__):
            
            def _check_dict(a: Dict,b: Dict) -> bool:
                # Check if labels / columns are equal
                if a.keys() != b.keys(): return False

                # Check if arrays are equal
                checks = []
                for arr1, arr2 in zip(a.values(), b.values()):
                    if arr1.dtype != arr2.dtype: return False
                    if arr1.dtype.type is np.str_:
                        checks.append(np.array_equal(arr1,arr2))
                    else:
                        checks.append(np.allclose(arr1,arr2, rtol=1e-08))
                if not all(checks): return False
                return True
            
            # Both are empty
            if (not self._data) and (not other._data): return True
            # One is empty
            if (not self._data) or (not other._data): return False

            # Check data
            if not _check_dict(self._data, other._data): return False
            # Check labels
            if not all(self._labels == other._labels): return False
            # Check shape
            if not self.shape == other.shape: return False
            
            return True
        
        else:
        
            return False
    
    def __ne__(self, other):
        return not self.__eq__(other)

    
    def get_column(self,label):
        return DataTable._from_dict({label:self._data[label]})
    