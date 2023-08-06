# pbar-parallel
PBar parallel is a simple wrapper around joblib, that shows you how many jobs 
have been processed in a simple progress by.

## Install
```pip install pbar-parallel```

## Usage

````python
from pbar_parallel import PBarParallel, delayed

def func(x):
    return x**2

prl = PBarParallel(n_jobs=48)
result = prl(total=1000)(delayed(func)(i) for i in range(1000))
````