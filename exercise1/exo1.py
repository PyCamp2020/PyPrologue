# -*- coding: utf-8 -*-
"""
Python 练习一

计算年均雨量

@author: si
"""

# 引入相关库
import os
import pandas


def getCwd():
    return os.getcwd()


"""
获取当前路径

@note Python 中变量无需声明， 可以直接赋值
"""
print(getCwd())

# 改变工作路径到 data
os.chdir(path='F:\PyPrologue\data')

# 列出当前路径下的内容
os.listdir()


# 小知识： 编程语言都是显式的 (explicit)
"""
========
读取数据
========

1. 分隔符:
    我们在读取一个 CSV 文件时， 首先要注意它的分隔符是否为 `pandas.read_csv()` 默认的 ','， 若不是，
    我们则用 `sep` 这一参数来指定我们文件中的分隔符， 例如 `sep=';'`.
2. 忽略注释行：
    `pandas.read_csv()` 方法， 可以通过指定 `comment` 参数来指定注释符号
3. 指定表头(列名称)所在行：
    使用 `header` 这一参数
4. 指定想导入的列:
    使用 `usecols` 这一参数
"""
df_raw = pandas.read_csv('BV_38.txt',
                         comment='#', 
                         usecols=['Date','Q','Ptot'],
                         header=0, sep=';', skipinitialspace=True)

df_neat = df_raw.dropna()
