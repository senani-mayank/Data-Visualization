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

def skip_initial_lines( file, file_delimiter ):
    line = file.readline()
    while (line != "") and (line.split( file_delimiter )[0].strip() != "TIME") :
        line = file.readline()
    if( line == "" ):
            return False
    return True


def getBadFlagValue( file_path, bad_flag ):
    bad_value = "not found"
    file = open( file_path  )
    line = file.readline()
    while line != "":
        pair = line.split(":")
        if( pair[0].strip() == bad_flag ) :
            bad_value = pair[1].strip()
            break;
        line = file.readline()
    file.close()
    return bad_value

def read_file_pandas() :
    df = pd.read_csv (file_path, skiprows=8, sep='\t', index_col='  ')

def omit_bad_values( array, bad_value  ):
    nrow = len(array)
    ncol = len(array[0])
    for i in range(nrow):
        for j in range(ncol):
            if array[i][j] == bad_value:
                array[i][j] = float('nan')

def get_lat_long_data( file_path, file_delimiter,metadata_delimiter ):
    file = open( file_path )
    line = ""
    skip_initial_lines( file, metadata_delimiter )
    longitudes = str(file.readline()).replace( '\n', '').split(file_delimiter)
    latitudes = []
    data = []
    while True :
        line = file.readline()
        if line == "":
            break
        line = str(line).replace('\n', '').split( file_delimiter )
        latitudes.append( line[0] )
        if( len(line) > 1 ):
            data.append( line[ 1 :  ] )
    if( latitudes[ len(latitudes) - 1 ] == '' ):
        latitudes.pop()

    longitudes = longitudes[ 1 :   ]
    return [ latitudes, longitudes, data]

def perform_task1( array, intp_method, cmap  ):

    for i in range(len(array)):
        for j in range(len(array[0]) ):
            array[i][j] = float(array[i][j])
    plt.imshow( array, cmap=cmap, interpolation=intp_method )
    plt.show()

def perform_task2( values, scaler_function  ) :
    latitudes = values[0]
    longitudes = values[1]
    for i in range(len(latitudes)):
        if 'N' in latitudes[i]:
            latitudes[i] = float( str(latitudes[i]).replace("N", "" ) )
        elif 'S' in latitudes[i] :
            latitudes[i] = float( "-" + str(latitudes[i]).replace("S","") )
    for i in range(len(longitudes)):
        if 'E' in longitudes[i]:
            longitudes[i] = float( str(longitudes[i]).replace("E","")  )
        elif 'W' in longitudes[i]:
            longitudes[i] = float( "-" + str(longitudes[i]).replace("W","") )
    X = []
    Y = []
    Z = []

    for i in range( len(latitudes) ):
        for j in range(len(longitudes)):
            values[2][i][j] = float(values[2][i][j])
            X.append( latitudes[i] )
            Y.append( longitudes[j] )
            if math.isnan(values[2][i][j]) :
                values[2][i][j] = float(0)
            Z.append( values[2][i][j] )

    #plot_surface( np.array(values[0]),np.array(values[1]), values[2])
    plot_surface_new(X,Y,Z)

def plot_surface( X,Y,Z  ) :
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(X,Y)
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    plt.show()

def plot_surface_new( x,y,z  ):
    df = pd.DataFrame({'x': x, 'y': y, 'z': z})
    fig = plt.figure()
    ax = Axes3D(fig)
    surf = ax.plot_trisurf(df.x, df.y, df.z, cmap=cm.jet, linewidth=0.1)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.savefig('teste.pdf')
    plt.show()

folder_path = '../dataset'
file_name = 'Aug-2016-tropical-heat-potential-180x188.txt'
file_path = folder_path + "/" + file_name
file_delimiter = "\t"
metadata_delimiter = ":"
bad_flag = "BAD FLAG"
values = get_lat_long_data(file_path, file_delimiter, metadata_delimiter)
bad_flag_value = getBadFlagValue( file_path, bad_flag  )

omit_bad_values(values[2], bad_flag_value  )
#perform_task1( values[2], INTP_METHODS[1], COLOR_SPECTRUMS[1]  );
perform_task2(values, "")
