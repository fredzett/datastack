# datastack
DataStack makes it easy to do data analysis as a first time coder.

More to follow.

**How to use**

1. Jupyter Notebook

```python
import sys
!{sys.executable} -m pip install git+"https://github.com/fredzett/datastack"

from datastack import DataTable, DataColumn, col, label
import numpy as np

# Create Table with 1 Mio rows
n = 1_000_000
tbl = DataTable(a=np.random.choice(range(100),n),
                b=np.random.rand(n),
                c=np.random.choice(range(100),n),
                d=np.random.choice(list("abcefdsgekd"), n))

# Apply verbs
tbl = (tbl
        .filter(col("c").larger_then(3.5)) 
        .mutate(NewCol=col("c") * col("a") * 12.24)
        .order_by(label("c"), label("NewCol"), asc=[True, False])
        .select(label().contains("New") | label("c"))
        )
```