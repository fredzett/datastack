import pandas as pd
import numpy as np

class Sheet:
    def __init__(self, **columns):
    'some comment'

        self._labels = []
        self._data = {}
        self._load_raw(columns)
    
    @classmethod
    def from_raw(cls,**columns):
        print(columns)
        return cls(**columns)#._load_raw(columns)

    @classmethod
    def from_csv(cls,fname,**kwargs):
        df = pd.read_csv(fname,**kwargs)
        return df


    # loads raw data in
    def _load_raw(self, columns):

        # Store length of first columns
        self._n = len(list(columns.values())[0])
        
        # Loop through columns and load into data structure
        for label, coldata in columns.items():

            # Sanity checks
            if label in self._labels:
                raise ValueError("Column already exists in dataframe")
            
            if len(coldata) != self._n:
                raise ValueError("All columns must be of same length")

            # add label to labels
            self._labels.append(label)

            # update internal dictionary
            self._data[label] = np.array(coldata)
        
    def __len__(self):
        return self._n

    def size(self):
        return (len(self),len(self._labels, ))



    #def filter(self,*fns):
    #    data = self._data 
    #    for f in fns:


        