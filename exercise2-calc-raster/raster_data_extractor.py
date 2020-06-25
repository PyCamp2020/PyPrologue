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


    """
    @brief 数据是否成功加载
        Python 中 getter, setter 等计算属性可以通过 @property 修饰符去定义
    """
    @property
    def data_loaded(self):
        return not (self.data is None)


    def _parse_header_line(self, line):
        token =  line[0].lower() if type(line[0]) == 'str' else None
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
        if self.dx > 0 and self.dx > 0 and self.nrows > 0 and self.ncols > 0:
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
        return None

    
    """
    @brief 从数据中提取相应坐标点 (x, y) 上的数据
    @param x - 查询点的横坐标
    @param y - 查询点的纵坐标
    """
    def extract(self, x, y):
        if (self.data_loaded):
            return 1.
        return None

