#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 20:46:31 2020

@author: niko
"""

import numpy as np


class RasterDataExtractor:

    # @constructor
    def __init__(self, fname):
        self.ncols              = 0         # number of columns
        self.nrows              = 0         # number of rows
        self.x0                 = 0         # the upper-left corner x coordinate
        self.y0                 = 0         # the upper-left corner y coordinate
        self.dx                 = 0         # cell x resolution (either in meter or degree)
        self.dy                 = 0         # cell y resolution (either in meter or degree)
        self.nodata_value       = 0         # NO-DATA value flag
        self.aaigrid_datatype   = "float32" # data type of the raster's field

        self.fname              = fname     # cache ASCII Grid file name
        self.dem                = None      # file handle to the ASCII Grid file
        self.header_row_count   = 0         # 记录栅格数据文件头的行数
        self.data               = None
        self.data_ready_flag    = False

        self.dem = open(self.fname, 'r')
        self.parse_head()
        self.parse_data()
        self.dem.close()


    """
    @brief 数据是否成功加载
        Python 中 getter, setter 等计算属性可以通过 @property 修饰符去定义
    """
    @property
    def data_loaded(self):
        return not (self.data is None)

    """
    @brief 返回栅格数据的包围体
        (xmin, ymin, xmax, ymax)
    """
    @property
    def extent(self):
        return (
            self.x0,
            self.y0,
            self.x0 + self.dx * self.ncols,
            self.y0 + self.dy * self.nrows
        )


    def _parse_header_line(self, line):
        token =  line[0].lower() if type(line[0]) == str else None
        if token == 'ncols':
            self.ncols = int(line[1])
        elif token == 'nrows':
            self.nrows = int(line[1])
        elif token == 'xllcorner':
            self.x0 = float(line[1])
        elif token == 'yllcorner':
            self.y0 = float(line[1])
        elif token == 'dx':
            self.dx = float(line[1])
        elif token == 'dy':
            self.dy = float(line[1])
        elif token == 'cellsize':
            self.dx = self.dy = int(line[1])
        elif token == 'nodata_value':
            self.nodata_value = int(line[1])
        else:
            return None
        return None


    """
    @brief 判断 (x, y) 是否在我们的栅格数据中
    """
    def _is_inside(self, x, y):
        ext = self.extent
        if ext[0] > x or ext[1] > y or ext[2] < x or ext[3] < y:
            return False
        return True

    """
    @brief 获取行和列的辅助函数
    """
    def _get_row(self, y):
        return int( (y - self.y0) / self.dy )
    def _get_col(self, x):
        return int( (x - self.x0) / self.dx )


    """
    @brief 读取栅格文件的头   栅格
        @ncols          栅格文件总列数
        @nrows          栅格文件总行数
        @xllcorner      左上角角点 x 坐标
        @yllcorner      左上角角点 y 坐标
        @[dx]           栅格 x 方向分辨率
        @[dy]           栅格 y 方向分辨率
        @[cellsize]     栅格分辨率, 当 dx==dy 时使用该关键字
        @no_data_value  无数据时的栅格值
    """
    def parse_head(self):
        for i in range(10000):
            line = self.dem.readline().split()
            if len(line) == 0:
                self.header_row_count = i
                break
            self._parse_header_line(line)

        # 检查数据正确性
        if self.dx > 0 and self.dy > 0 and self.nrows > 0 and self.ncols > 0:
            return None

        errMsg = \
            """栅格文件 '{fname}' 格式异常:
                   nrows = {nrows}
                   ncols = {ncols}
                   dx    = {dx}
                   dy    = {dy}
            """.format(
                    fname=self.fname,
                    nrows=self.nrows,
                    ncols=self.ncols,
                    dx=self.dx,
                    dy=self.dy
                )
        # 数据不正确直接抛出异常
        raise Exception(errMsg)


    """
    @brief 读取栅格数据
    """
    def parse_data(self):
        self.data = np.loadtxt(fname=self.fname, skiprows=self.header_row_count)
        return None


    """
    @brief 从数据中提取相应坐标点 (x, y) 上的数据
    @param x - 查询点的横坐标
    @param y - 查询点的纵坐标
    """
    def extract(self, x, y):
        if self.data_loaded:
            if not self._is_inside(x, y):
                return None
            irow = self._get_row(y)
            icol = self._get_col(x)
        return self.data[irow,icol]



# # 测试我们的栅格数据提取器, 当运行这个文件时, python 会执行下面这两句
# file_path = '/home/niko/Documents/PyCamp2020/data/eat8a_WDraster_PEAK_test.asc'
# extractor = RasterDataExtractor(file_path)
# print( "extractor.data_loaded: {0}".format(extractor.data_loaded) )



# """ 
# 字符串格式化的几种方式:
#     1. 使用键值查找相应需要格式化的变量
#     2. 使用相应变量的位置索引格式化变量
# """
# test_str = '环宇有 {number_of_eyes} 个眼睛, {y} 个腿儿'.format(number_of_eyes=2, y=2)
# test_str = '环宇有 {0} 个眼睛, {1} 个腿儿, {2} 个鼻子'.format(6, 8, 1, 1321)


# """
# Python 中字符串的声明方式:
#     1. 常用的单引号声明 : '{字符串内容}'
#     2. 常用的双引号声明 : \"{字符串内容}\"
#     3. 常用的三引号声明 : \"\"\"{字符串内容}\"\"\"
#         三引号声明可以自动捕捉代码中的换行符 '\n', 打印多行内容时比较方便
# """
