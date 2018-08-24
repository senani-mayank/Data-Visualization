import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as col
#import string

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
    return [ latitudes, longitudes, data  ]

folder_path = '../dataset'
file_name = 'Aug-2016-tropical-heat-potential-180x188.txt'
file_path = folder_path + "/" + file_name
file_delimiter = "\t"
metadata_delimiter = ":"
bad_flag = "BAD FLAG"
values = get_lat_long_data(file_path, file_delimiter, metadata_delimiter)
bad_flag_value = getBadFlagValue( file_path, bad_flag  )

omit_bad_values(values[2], bad_flag_value  )
for i in range(len(values[2])):
    for j in range(len(values[2][0])):
        values[2][i][j] = float(values[2][i][j])
plt.imshow( values[2] )
plt.show()
