import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as col
import math
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
#import string

INTP_METHODS = ["bilinear", "bicubic"]
COLOR_SPECTRUMS = ["rainbow", "gray", "BuGn"]
FILE_NAMES = [ "Aug-2016-meridional-current-181x189", "Aug-2016-potential-temperature-180x188", "Aug-2016-salinity-180x188", "Aug-2016-tropical-heat-potential-180x188", "Aug-2016-zonal-current-181x189" ]

BAD_FLAG_KEY = "BAD FLAG"
folder_path = '../dataset'
file_name = FILE_NAMES[0]
file_path = folder_path + "/" + file_name + ".txt"

def get_bad_flag( BAD_FLAG_KEY, file_path ):
	bad_flag = "NA"
	file = open( file_path )
	for line in file:
		if BAD_FLAG_KEY in line:
			flag = line.split(":")[1]
			bad_flag = flag.strip()
			break
	file.close()
	return bad_flag
	
def get_lines_to_skip( file_path ):
	bad_flag = "NA"
	i=0
	file = open( file_path )
	for line in file:
		split = line.split(":")
		if len(split) < 2 : 
			break
		i = i + 1
	file.close()
	return i

def read_file( file_path, lines_to_skip ) :
    return pd.read_csv (file_path, skiprows=lines_to_skip, sep='\t')

def mask_array( array, mask_value ):
	return np.ma.masked_equal(data, mask_value )
	

bad_flag = get_bad_flag( BAD_FLAG_KEY, file_path )
num_lines_to_skip = get_lines_to_skip( file_path )
data = read_file( file_path, num_lines_to_skip )

#extract longitudes
longitudes = np.array(data.columns.values)
#get firts column key to extract latitudes
first_cloumn_key = longitudes[0]
#remove first element
longitudes = longitudes[1:]
#extract latitudes
latitudes = np.array( data[first_cloumn_key]  )
#delete first clumn
data = data.drop(columns=first_cloumn_key)
#convert data to numpy 2D array
data = np.array(data)
#mask bad values
data = mask_array( data, float(bad_flag.strip()) )
print(  data )
#with open('your_file.txt', 'w') as f:
#    for item in data:
#        f.write("%s\n" % item)