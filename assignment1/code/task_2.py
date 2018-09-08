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
	
def perform_task( latitudes, longitudes, array,  cmap, func_type  ):
	
	X= latitudes
	Y= longitudes

	X, Y = np.meshgrid(X, Y)
	Z = np.array(array)
	if func_type == 'exp' :
		Z = np.exp( Z )
	Z = np.transpose(Z)
	Z = np.ma.masked_invalid(Z)
	fig = plt.figure()
	ax = plt.axes(projection='3d')
	ax.plot_surface(X, Y, Z)
	plt.show()

	'''
	X = []
	Y = []
	Z = []
	for i in range( len(latitudes) ):
		for j in range(len(longitudes)):
			X.append( latitudes[i] )
			Y.append( longitudes[j] )
			Z.append(array[i][j]  )
	df = pd.DataFrame({'x': X, 'y': Y, 'z': np.ma.masked_invalid(Z) })
	fig = plt.figure()
	ax = Axes3D(fig)
	surf = ax.plot_trisurf(df.x, df.y, df.z, cmap=cm.jet, linewidth=0.001)
	fig.colorbar(surf, shrink=0.5, aspect=5)
	plt.show()
	'''

def normalize_values( array ):
	min = np.nanmin(array)
	max = np.nanmax(array)
	if max == min :
		return
	for i in range( len(array) ):
		for j in range( len(array[0]) ):
			array[i][j] = (array[i][j] - min) / ( max - min )

def normalize_values_1d( array ):
	min = np.nanmin(array)
	max = np.nanmax(array)
	if max == min :
		return
	for i in range( len(array) ):
		array[i] = (array[i] - min) / ( max - min )
			
def custom_color_map( c_name,c_dict ):
	#https://matplotlib.org/gallery/images_contours_and_fields/custom_cmap.html
	return col.LinearSegmentedColormap( c_name, c_dict)
	

bad_flag = get_bad_flag( BAD_FLAG_KEY, file_path )
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
#normalize data(all values between 0-1)
normalize_values( data )

#mask bad values
data = np.ma.masked_invalid( data )
#format_latitudes
format_latitudes(latitudes)
format_longitudes(longitudes)
normalize_values_1d(latitudes)
normalize_values_1d(longitudes)
perform_task( latitudes, longitudes, data, custom_color_map( "BlueGreen" ,cdict_BuGn), 'exp' )
with open('your_file.txt', 'w') as f:
    for item in data:
        f.write("%s\n" % item)