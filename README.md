# TUTORIAL: How to use DistComp

Author:  OR KOREN <or.koren@shutterfly.com>

---

## Installation

```bash
  $ pip install git+ssh://git@gh.internal.shutterfly.com/or-koren/distcomp.git
```

### Quick Start

###### creating a dummy df for the example
```python
def DummyDF(n=1):
    
    df = pd.DataFrame(index=range(n))
    # create normal dist with mean 10 and SD 2 
    df['feature_A'] = np.random.normal(loc=0,scale=1,size=df.shape[0])
    df['feature_B'] = np.random.normal(loc=0.5,scale=1.2,size=df.shape[0],)

    l=['test' for i in range(int(0.8*n))]+['ctrl' for i in range(int(0.2*n))]
    df['treatment'] = l
    
    df['Feature_C'] = pd.concat([df[df.treatment=='test']['feature_A'],df[df.treatment=='ctrl']['feature_B']])

    return df

df=DummyDF(n=50000)
```    
---
###### actual usage once you have a dataframe with features and an optional treatment column (e.g. test/control column)

```python
from distcomp import comparing_distributions

cd=comparing_distributions(df,
                           features=['feature_A','feature_B','Feature_C'],
                           treatment='treatment',
                           sample_frac=0.8,
                           remove_outliers_quintiles=[0.01,0.99])
                           

# functions from the module 

# histnorm accept percent/probability/density/probability density/None
cd.PlotHist(histnorm='probability density',bins=None)

cd.PlotECDF(figsize=(10,4))

cd.KS_Test(pval=0.1,ks_alternative='two-sided',ks_mode='auto')

cd.ttest(test_group_name='test',pval=0.05)

cd.create_table_one(test_group_name='test')

```
