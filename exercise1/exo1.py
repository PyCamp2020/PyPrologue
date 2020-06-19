# -*- coding: utf-8 -*-
"""
@breif Python 练习一
@author si.chen

目标: 计算某一流域的年均雨量

知识点:
	1. 如何导入一个库				:	import 	语句
	2. 如何定义方法(函数)			:	def 	语句
	3. 如何定义变量				:	<变量名> = <值>
	4. 使用 os 模块中路径相关操作	:	getcwd(), listdir(), chdir() 方法
	5. 如何使用 pandas 库读取 csv 	:	read_csv() 方法
	6. 去掉 DataFrame 中的缺失行	:	dropna() 方法
"""


# 引入相关库
import os
import pandas


"""
============
定义方法(函数)
============

Python 中使用 `def` 关键字来定义函数, 格式如下:

def <函数名>([<参数1>, <参数2>...<参数n>]):
	<函数定义>
	return <返回值>

例如我们在这里定义一个 `get_cwd()` 方法, 用于获取当前工作路径,
作为 `os.getcwd()` 的短手 (short-hand)

"""
def get_cwd():
    return os.getcwd()


# Python3 中打印方法为 print()
print("当前工作路径 = ")
print(get_cwd())

# 列出初始工作路径下的内容
print("当前路径下的内容 = ")
os.listdir()

# 改变工作路径到 data
os.chdir(path='F:\PyPrologue\data')
print("我们改变后的工作路径 = ")
print(get_cwd())

# 列出路径下的内容
print("当前路径下的内容 = ")
os.listdir()


# 小知识： 编程语言都是显式的 (explicit)
"""
=======
读取数据
=======

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
df_raw = pandas.read_csv(
	'BV_38.txt',
    comment='#',
    sep=';', 
    header=0,
    usecols=['Date','Q','Ptot'],
    skipinitialspace=True
)

# 去掉 DataFrame 中的缺失行, `inplace` 参数代表是否直接在原变量中操作
df_raw.dropna(inplace=True)

#完成读取数据，清理无效条目
print(df_raw)

print(type(df_raw))
print(df_raw.index)

#整理数据类型
#将数据类型转化为时间日期类型
df_raw['Date']=pandas.to_datetime(df_raw['Date'])

#将date设置为index
df=df_raw.set_index('Date')
print(df_raw)
print(df.shape)

#构造series数据类型
s=pandas.Series(df['Q'])
print(type(s))

#获取1961年的数据
print('----------获取1961年的数据-------')
print(df['1961'])

#获取某月的数据
print('----------获取1961年5月的数据-------')
print(df['1961-5'])


#利用groupby分组求年平均值
M = df_raw.groupby(pandas.Grouper(freq='Y')).mean
print(M)


"""
#按照年进行统计
dfY=df_raw.resample ('Y').mean()
dfY[['Q','Ptot']]=dfY[['Q','Ptot']].applymap()
#保存年平均数据
dfY.to_csv('F:\PyPrologue\data\年平均值.csv')

"""


























