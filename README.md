# datastack
DataStack makes it easy to do data analysis as a first time coder.

More to follow.

**How to use**

1. Jupyter Notebook

```python
import sys
!{sys.executable} -m pip install git+"https://github.com/fredzett/datastack"

from datastack import DataTable, DataColumn, col, labels

tbl = DataTable(a=[1,2,3], b=[4,5,6])
```