# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 13:19:12 2020

@author: Administrator
"""


import pandas
import os
import numpy


def get_cwd():
    return os.getcwd()

print(get_cwd())
os.chdir(r'F:\PyPrologue\data')
print(get_cwd())


df_raw = pandas.read_csv(
	'BV_38.txt',
    comment='#',
    sep=';', 
    header=0,
    usecols=['Date','Q','Ptot'],
    skipinitialspace=True
)
df_raw.dropna(inplace=True)


#日期格式的转化
df_raw['Date']=pandas.to_datetime(df_raw['Date'])
df=df_raw.set_index('Date')
df.head(3)

