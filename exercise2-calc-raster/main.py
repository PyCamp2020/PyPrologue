from raster_data_extractor import RasterDataExtractor as Extractor
import os, re
from pathlib import Path, PurePath
import numpy as np
import pandas


"eat8a_WDraster_3600.asc"
"eat8a_WDraster_[[0-9]+].asc"


# 数据根目录
data_path = "/home/niko/Documents/test_data"


# caflood 项目名称
project_name = "eat8a"
# caflood 文件名通用分隔符
sep = "_"
# caflood 输出变量名称
var_name = "VEL"
# caflood 输出文件类型
file_type_name = "raster"
# caflood 输出帧
frame_index = 0
# 帧数正则表达式
frame_regex = "([0-9]+)"
# 文件后缀
file_ext = '.asc'


"""
@brief 根据文件名的正则表达式, 匹配目标目录下所有的相应数据文件
    regular expression
"""
restr = project_name    + \
        sep             + \
        var_name        + \
        file_type_name  + \
        sep             + \
        frame_regex     + \
        file_ext

regex = re.compile(restr)


# 读取目标目录下所有内容
contents = os.listdir(data_path)

# 目标数据文件名列表
files = []


"""
@brief 找到文件名中的时间, 并转化成整数返回
"""
def find_frame(fname):
    if type(fname) is str:
        idot = fname.rfind('.')
        ilodash = fname.rfind('_')
        if idot < len(fname) and ilodash < len(fname) and ilodash < idot:
            return int(fname[ilodash+1:idot])
    return None


# 迭代目标目录下所有的文件, 并将符合要求的文件加入到 `files` 列表中
for fname in contents:
    if regex.match(fname) is None:
        continue
    file_path = Path(data_path, fname)
    if file_path.is_file():
        files.append(file_path.__str__())

files.sort(key=find_frame)


points_fname = "/home/niko/Documents/test_data/WDpoints.csv"
points = pandas.read_csv(
        points_fname,
        skipinitialspace=True,
        skiprows=[0, 1],
        nrows=2
    ).iloc[:, 1:]


"""
@brief 循环遍历所有栅格数据文件, 每一次数据读取成功后, 提取相应的一系列数据点
"""
all_results = []
row_names = []
for file in files:
    e = Extractor(file)
    point_result = []
    for point_name in points:
        val = e.extract(points[point_name][0], points[point_name][1])
        point_result.append(val)
    all_results.append(point_result)
    fpath = Path(file)
    fname = fpath.name
    fsuffix = fpath.suffix
    row_names.append( fname[0:fname.rfind(fsuffix)] )


# 最后的结果表格
final_df = pandas.concat(
        [points, pandas.DataFrame(all_results, columns=points.columns)],
        ignore_index=True,
        sort=False
    )

# 结果文件行名称
final_row_names = ["X", "Y"] + row_names

# 重新赋值每一行的名称
final_df.set_index(pandas.Series(final_row_names), inplace=True)

# 重命名结果表格的行名称
final_df.rename_axis("point name", axis='columns')

# 结果文件名
result_fname = project_name + sep + var_name + ".csv"

# 保存结果文件
final_df.to_csv(Path(data_path, result_fname))

