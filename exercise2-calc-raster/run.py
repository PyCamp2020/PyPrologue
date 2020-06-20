import numpy as np
import sys


# input file (absolute) path, remember to change it to you proper path!
file_path = '/home/niko/Documents/PyCamp2020/data/eat8a_WDraster_PEAK.asc'

# create a file handle
dem_file = open(file_path, 'r')

# new_line_char = '\n'


'''
    Begin to parse AAIGrid – Arc/Info ASCII Grid
'''

# use seek(0) method to roll back to the file's head
dem_file.seek(0)


# global scope
# read AAIGrid's characteristic variables
ncols         = 0;  # number of columns
nrows         = 0;  # number of rows
x0            = 0;  # the upper-left corner x coordinate
y0            = 0;  # the upper-left corner y coordinate
cellsize      = 0;  # size of the grid cell (either in meter or degree)
NO_DATA_VALUE = 0;  # NO-DATA value flag


'''
@brief Helper function to read asc grid characteristic variables

@param line - array of strings that represents a line in a '.asc' file
'''
def parse_var(line):
    global ncols
    global nrows
    global x0
    global y0
    global cellsize
    global NO_DATA_VALUE
    token = line[0]
    if token == 'ncols':
        ncols = int(line[1])
    elif token == 'nrows':
        nrows = int(line[1])
    elif token == 'xllcorner':
        x0 = float(line[1])
    elif token == 'yllcorner':
        y0 = float(line[1])
    elif token == 'cellsize':
        cellsize = int(line[1])
    elif token == 'NODATA_value':
        NO_DATA_VALUE = int(line[1])
    else:
        return None
    return None


try:
    for i in range(1000):
        tokens = dem_file.readline().split()
        token_count = len(tokens)
        if token_count == 0:
            break
        parse_var(tokens)
except:
    print("Unexpected error:", sys.exc_info()[0])
    dem_file.close()



# close the file stream when data reading is done. important!
dem_file.close()
