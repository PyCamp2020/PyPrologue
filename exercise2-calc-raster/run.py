import numpy as np
import sys


# input file (absolute) path, remember to change it to you proper path!
file_path = '/home/niko/Documents/PyCamp2020/data/eat8a_WDraster_PEAK_test.asc'

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
    # Given that an ASCII Grid file's head is less than 1000 rows,
    # we will seek exhaustively the header's last row index in the following loop
    for i in range(1000):
        tokens = dem_file.readline().split()
        token_count = len(tokens)
        if token_count == 0:
            break
        parse_var(tokens)

except:
    print("Unexpected error:", sys.exc_info()[0])
    dem_file.close()



"""
@brief Given any point with coordinate(x, y), interpolate its value on the raster
"""

# Point(x=100, y=100)
p = [x0 + 4 * 2, y0 + 4. * 5]   # Array representation of a 2D-point, 0.091930
# p = {'x': 100., 'y': 100.}        # Object-like representation of a 2D-Point

# find the row index of the given point
irow = (p[1] - y0) / cellsize
icol = (p[0] - x0) / cellsize


# helper function to check if the query point is valid
def checkIndicesValidity(i, i_max):
    global p
    global valid
    if i < 0 or i > i_max:
        print("Point (", p[0], ", ", p[1], ") out of bounds!")
        valid = False


# irow, icol is now a floating-point number, we want to check there viablilities
valid = True
checkIndicesValidity(irow, nrows)
checkIndicesValidity(icol, ncols)

# extract corresponding values on the raster at point `p`
if valid:
    # do the extraction:
    #   method 1: each time read the .asc file to extract value, not recommended in our case
    #   method 2: load, with a single read, all the values of the raster file into an array
    raster_data = np.loadtxt(fname=file_path, skiprows=i)
    print("data(x=", p[0], ",y=", p[1], ") = ", raster_data[int(irow)][int(icol)])



"""
@brief extract data from a 2D raster
"""


# close the file stream when data reading is done. important!
dem_file.close()
