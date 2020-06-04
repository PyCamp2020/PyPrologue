# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import pandas
import numpy as np

os.chdir("/home/huanyu/Documents/myProjects/PyPrologue/")

# df_all_cols = pandas.read_csv('data/BV_38.txt', sep=";", comment="#")

df_PQ = pandas.read_csv('data/BV_38.txt', sep=";", comment="#",
                        usecols=["Date", "Q", "Ptot"], 
                        header=0, names=["Date", "Q", "Ptot"],
                        na_values='NA', keep_default_na=False,
                        skipinitialspace=True,
                        dtype={'Q':np.float64, 'Ptot':np.float64})

df_PQ
