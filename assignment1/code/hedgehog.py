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
FILE_NAMES = [ "aug_6_temp","Aug-2016-meridional-current-181x189", "Aug-2016-potential-temperature-180x188", "Aug-2016-salinity-180x188", "Aug-2016-tropical-heat-potential-180x188", "Aug-2016-zonal-current-181x189" ]


cdict_gray = {'red':  ((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0)),

         'green': ((0.0, 0.0, 0.0),
                  (1.0, 1.0, 1.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0))
        }
		
cdict_BuGn = {'green':   ((0.0, 0.0, 1.0),
                   (1.0, 0.0, 0.0)),

         'red': ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0))
        }

cdict_rainbow = {'red':   ((0.0, 0.0, 1.0),
                   (0.2, 1.0, 1.0),
				   (0.4, 0.0, 0.0),
				   (0.6, 0.0, 0.0),
				   (0.8, 0.0, 0.0),
                   (1.0, 1.0, 0.0)),

         'green': ((0.0, 0.0, 0.0),
                   (0.2, 1.0, 1.0),
				   (0.4, 1.0, 1.0),
				   (0.6, 1.0, 1.0),
				   (0.8, 0.0, 0.0),
                   (1.0, 0.0, 1.0)),
                   
         'blue':  ((0.0, 0.0, 0.0),
                   (0.2, 0.0, 0.0),
				   (0.4, 0.0, 0.0),
				   (0.6, 1.0, 1.0),
				   (0.8, 1.0, 1.0),
                   (1.0, 1.0, 1.0)),
        }
		
		
BAD_FLAG_KEY = "BAD FLAG"
folder_path = '../dataset'
file_name = FILE_NAMES[2]

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

def read_file( file_path, lines_to_skip, bad_flag ) :
    return pd.read_csv (file_path, skiprows=lines_to_skip, sep='\t', na_values=[bad_flag])

def mask_array( array, mask_value ):
	return np.ma.masked_equal(data, mask_value )

def format_latitudes( latitudes ):
    for i in range(len(latitudes)):
        if 'N' in latitudes[i]:
            latitudes[i] = float( str(latitudes[i]).replace("N", "" ) )
        elif 'S' in latitudes[i] :
            latitudes[i] = float( "-" + str(latitudes[i]).replace("S","") )

def format_longitudes( longitudes ):
    for i in range(len(longitudes)):
        if 'E' in longitudes[i]:
            longitudes[i] = float( str(longitudes[i]).replace("E","")  )
        elif 'W' in longitudes[i]:
            longitudes[i] = float( "-" + str(longitudes[i]).replace("W","") )
	
def perform_task( latitudes, longitudes, datau,datav  ):
	X= latitudes
	Y= longitudes
	print(X.shape, Y.shape)
	UV = (datau**2 + datav**2) ** 0.5
	plt.title('HEDGEHOG PLOT')
	Q = plt.quiver( X[::5][0], Y[::5][0], datau[::5][0], datav[::5][0],UV[::5][0], scale=20 )
	plt.show()
	
def normalize_values( array ):
	min = np.nanmin(array)
	max = np.nanmax(array)
	if max == min :
		return
	for i in range( len(array) ):
		for j in range( len(array[0]) ):
			array[i][j] = (array[i][j] - min) / ( max - min )

def normalize_values_1d( array ):
	print array
	min = np.nanmin(array)
	max = np.nanmax(array)
	if max == min :
		return
	for i in range( len(array) ):
		array[i] = float(array[i]) - float(min) / ( float(max) - float(min) )
			
def custom_color_map( c_name,c_dict ):
	#https://matplotlib.org/gallery/images_contours_and_fields/custom_cmap.html
	return col.LinearSegmentedColormap( c_name, c_dict)

def get_lat_long_values(  bad_flag_key, folder_path, file_name ):
	
	file_path = folder_path + "/" + file_name + ".txt"
	bad_flag = get_bad_flag( bad_flag_key, file_path )
	num_lines_to_skip = get_lines_to_skip( file_path )
	data = read_file( file_path, num_lines_to_skip, bad_flag )
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
	#format_latitudes
	format_latitudes(latitudes)
	format_longitudes(longitudes)
	normalize_values_1d(latitudes)
	normalize_values_1d(longitudes)
	return [ latitudes, longitudes, data ]
	
datau = get_lat_long_values( BAD_FLAG_KEY, folder_path,FILE_NAMES[1] )
datav = get_lat_long_values( BAD_FLAG_KEY, folder_path,FILE_NAMES[5] )

#normalize data(all values between 0-1)
normalize_values( datau[2] )
#normalize data(all values between 0-1)
normalize_values( datav[2] )
print (datau[2].shape, datav[2].shape)
#mask bad values
datau[2] = np.ma.masked_invalid( datau[2] )
datav[2] = np.ma.masked_invalid( datav[2] )
perform_task( datau[0], datau[1], datau[2], datav[2]  )
with open('your_file.txt', 'w') as f:
    for item in datau:
        f.write("%s\n" % item)