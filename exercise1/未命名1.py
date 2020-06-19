# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 15:43:42 2020

@author: Administrator
"""


import pandas as pd
import numpy as np

index = pd.date_range('1/1/2000',periods=8)
s = pd.Series(np.random.rand(5),index=['a','b','c','d','e'])
s.head()

# .array用于提取Index或Series里的数据
# 提取Numpy数组，用to_numpy()
s.array
s.to_numpy()


dates = pd.date_range('20130101', periods=16)
df = pd.DataFrame(
    np.random.randn(16, 4),               
    index=dates,              
    columns=list('ABCD')
 )
df

# 显示索引与列名
df.index
df.columns
"""
df2 = pd.DataFrame({
    'A':1,
    'B':pd.Timestmap('20200601'),
    'C':pd.Series(1,index=list(range(4)),dtype='float32'),
    'D':np.array([3]*4,dtype='int32'),
    'E':pd.Categorical(["test","train","test","train"]),
    'F':'foo'
    } )
df2

df2.dtypes

















