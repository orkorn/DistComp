# distribution-comparison
---
# TUTORIAL: How to use DistComp

Author:  OR KOREN <or.koren@shutterfly.com>

## Installation

```bash
  $ pip install git+ssh://git@gh.internal.shutterfly.com/or-koren/distcomp.git
```

### Quick Start

```python
# dummy df function for demonstration 
def DummyDF(n=1):
    import pandas as pd 
    import numpy as pd
    df = pd.DataFrame(index=range(n))
    # create normal dist with mean 10 and SD 2 
    df['a'] = np.random.normal(loc=0,scale=1,size=df.shape[0])
    df['b'] = np.random.normal(loc=0.5,scale=1.2,size=df.shape[0])
    df['c'] = np.random.normal(loc=0.0,scale=1.1,size=df.shape[0])
    df['d'] = np.random.normal(loc=200,scale=11.5,size=df.shape[0])    

    l=['test' for i in range(int(0.8*n))]+['ctrl' for i in range(int(0.2*n))]
    df['gb_col'] = l
    return df
```    
---

```python
from distcomp import comparing_disterbutions


df=DummyDF(n=10000)
cd=comparing_disterbutions(df,
                           features=['a','b'],
                           treatment='gb_col',
                           sample_frac=0.9,
                           remove_outliers_quintiles=[0.01,0.99])
                           
# possible functions to use 
cd.PlotECDF()     
cd.PlotHist(histnorm='percent',bins=None)
cd.KS_Test(pval=0.1,ks_alternative='two-sided',ks_mode='auto')
cd.ttest()
cd.create_table_one(test_group_name='test')
```
