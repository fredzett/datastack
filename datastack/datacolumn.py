from __future__ import annotations


import numpy as np
from numbers import Number
from typing import Collection, Dict, Type, Union


def unpack1ddict(d: Dict):
    label, data = list(d.keys())[0], list(d.values())[0]
    return label, data

class DataColumn:
    '''DataColumn is a one dimensional data structure
    containing data array and a label'''
    def __init__(self, *label_and_column):
        if len(label_and_column) != 2:
            raise TypeError(f"DataColumn is created using two parameters (label, data). {len(label_and_column)} where provided.")
        label, data = label_and_column # unpack parameters
        self._label, self._data = self._check_and_convert(label, data)
        self._dtype = self._data.dtype.type

    def _check_and_convert(self, label, data) -> Union[str, np.ndarray]:
        'Ensures that parameters for DataColumn are of correct type and converts if not and possible'
        if not isinstance(label, str): 
            if isinstance(label, Number): 
                label = str(label)
            else:
                raise TypeError(f"Label of type {type(label)} cannot be stored in Column")
        if not isinstance(data, np.ndarray): 
            if isinstance(data, Number) or isinstance(data, str):
                data = np.asarray([data])
            elif isinstance(data, Collection):
                data = np.asarray(data)
            else:
                raise TypeError(f"Data of type {type(data)} cannot be stored in Column")
        return label, data


    def __repr__(self):
        return str(self.__dict__)

    def __len__(self) -> int:
        return len(self._data)

    ########################
    # From methods
    ########################

    @staticmethod
    def from_dict(**d: Dict) -> DataColumn:
        if len(d) > 1: raise ValueError("Dict must have one key only")
        label, data = unpack1ddict(d)
        return DataColumn(label, data)


    ########################
    # To methods
    ########################
    def to_dict(self):
        return {self._label:self._data}

    ########################
    # Comparison operators
    ########################

    def __eq__(self, other) -> DataColumn:
        'Checks elementwise if self(el) == other(el) and returns np.array with bools' 
        if isinstance(other, self.__class__):            
            if (self._dtype == np.str_) or (other._dtype == np.str_):
                out = [True if el1 == el2 else False for el1, el2 in zip(self._data, other._data)]
            else:
                out = self._data == other._data
        elif isinstance(other, Number):
            out = self._data == np.repeat(other, len(self))
        elif isinstance(other, str):
            out = np.array([True if el == other else False for el in self._data])
        else:
            raise TypeError(f"DataColumn cannot be compared with {type(other)}")

        return DataColumn("", out)

    def __ne__(self, other) -> np.ndarray:
        comp = self == other
        comp._data = ~comp._data 
        return comp

    def __gt__(self, other) -> DataColumn:
        'Checks elementwise if self(el) > other(el) and returns DataColumn with bools' 
        if isinstance(other, self.__class__):            
            if (self._dtype == np.str_) or (other._dtype == np.str_):
                raise TypeError(f"DataColumn(s) must be of numeric type to apply > check")
            else:
                out = self._data > other._data
        elif isinstance(other, Number):
            out = self._data > np.repeat(other, len(self))
        else:
            raise TypeError(f"DataColumn cannot be compared with {type(other)}")

        return DataColumn("", out)

    def __ge__(self, other) -> DataColumn:
        'Checks elementwise if self(el) > other(el) and returns DataColumn with bools' 
        if isinstance(other, self.__class__):            
            if (self._dtype == np.str_) or (other._dtype == np.str_):
                raise TypeError(f"DataColumn(s) must be of numeric type to apply > check")
            else:
                out = self._data >= other._data
        elif isinstance(other, Number):
            out = self._data >= np.repeat(other, len(self))
        else:
            raise TypeError(f"DataColumn cannot be compared with {type(other)}")

        return DataColumn("", out)

    def __lt__(self, other) -> DataColumn:
        return self > other # CHECK: why not other > self?

    def __le__(self, other) -> DataColumn:
        return self >= other # Check: why not other >= self?



    ########################
    # Base math operators
    ########################


    def __add__(self, other):
        if isinstance(other, self.__class__):
            self._data = self._data + other._data 

        elif isinstance(other, Number):
            self._data = self._data + other
        else:
            raise TypeError(f"Cannot add type {type(other)} to DataColumn")  

        return self

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            self._data = self._data - other._data 

        elif isinstance(other, Number):
            self._data = self._data - other
        else:
            raise TypeError(f"Cannot add type {type(other)} to DataColumn")  

        return self

    def __rsub__(self, other):
        return (self - other) * -1
        #if isinstance(other, self.__class__):
        #    self._data = other._data - self._data 
#
        #elif isinstance(other, Number):
        #    self._data = other - self._data 
        #else:
        #    raise TypeError(f"Cannot add type {type(other)} to DataColumn")  
#
        #return self


    def __mul__(self, other):
        if isinstance(other, self.__class__):
            self._data = self._data * other._data 

        elif isinstance(other, Number):
            self._data = self._data * other
        else:
            raise TypeError(f"Cannot add type {type(other)} to DataColumn")  

        return self

    def __rmul__(self, other):
        return self.__mul__(other)
   
    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            self._data = self._data / other._data 

        elif isinstance(other, Number):
            self._data = self._data / other
        else:
            raise TypeError(f"Cannot add type {type(other)} to DataColumn")  

        return self

    def __rtruediv__(self, other):
        if isinstance(other, self.__class__):
            self._data = other._data / self._data 
        elif isinstance(other, Number):
            self._data = other / self._data
        else:
            raise TypeError(f"Cannot add type {type(other)} to DataColumn")  
        return self

    def __pow__(self, other):
        if isinstance(other, self.__class__):
            self._data = self._data ** other._data 

        elif isinstance(other, Number):
            self._data = self._data ** other
        else:
            raise TypeError(f"Cannot add type {type(other)} to DataColumn")  

        return self


    def __rpow__(self, other):
        if isinstance(other, self.__class__):
            self._data = other._data ** self._data 

        elif isinstance(other, Number):
            self._data = other ** self._data 
        else:
            raise TypeError(f"Cannot pow type {type(other)} to DataColumn")  

        return self





    ########################
    # Iterator
    ########################
    def __iter__(self):
        print("MOIN!")
        return ColumnIterator(self)


    ########################
    # Other functions
    ########################
    def rename(self, name: str):
        self._label = name 
        return self

    def sum(self, skip_nan=False) -> Number:
        if self._dtype == np.str_: raise TypeError("Cannot apply sum to data consisting of strings")
        if skip_nan: 
            return np.nansum(self._data)
        else:
            return np.sum(self._data)

    def cumsum(self) -> DataColumn:
        if self._dtype == np.str_: raise TypeError("Cannot apply sum to data consisting of strings")
        return DataColumn("cumsum", self._data.cumsum())

    def lag(self, n: int) -> DataColumn:
        
        replace = np.nan
        data = self._data

        if self._dtype == np.str_: 
            replace = "nan"
        elif (self._dtype == np.int_) or (self._dtype == np.bool_):
            data = data.astype(float)


        if abs(n) > len(self): 
            raise ValueError(f"You can not calculate lag {n} for DataColumn with length {len(self)}")
        else:
            if n > 0:
                shifted = np.pad(data, (n,0), constant_values=replace)[:-n]
            elif n < 0:
                shifted = np.pad(data, (0,abs(n)), constant_values=replace)[abs(n):]
            else:
                shifted = self._data
        n = str(n) if n > 0 else f"neg{abs(n)}"
        return DataColumn("lag_" + n, shifted)


##### Utility functions for DataColumm

def are_equal(*cs: DataColumn) -> bool:
    'Checks if DataColumns are equal including label and returns True / False'
    first_col = cs[0]
    first_type = first_col._data.dtype.type
    for col in cs[1:]:
        if col._label == first_col._label:
            if (first_type == np.str_) or (col._data.dtype.type == np.str_):
                return np.array_equal(first_col._data, col._data)
            else:
                return np.allclose(first_col._data,col._data)
    return False


def are_not_equal(*cs: DataColumn) -> bool:
    return not are_equal(*cs)

class ColumnIterator:
    'Iterator class used by DataColumn'
    def __init__(self, dc: DataColumn):
        self._datacolumn = dc
        self._idx = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        if self._idx < len(self._datacolumn):
            result = self._datacolumn._data[self._idx]
        else:
            raise StopIteration
        self._idx += 1
        return result