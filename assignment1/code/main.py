def read_file( file_path ):
    file = open( file_path, 'r')
    i = 0;
    while i < 8 :
        print file.readline();
        i = i + 1
    longitudes = list(file.readline().split('\t'))
    latitudes = []
    for line in file :
        latitudes.append(line.split('\t')[0])
    print latitudes
    #print  len(file.readline().split('\t'))

folder_path = '/home/mayank/Desktop/DV/assignment1/dataset'
file_name = 'Aug-2016-potential-temperature-180x188.txt'
read_file( folder_path + '/' + file_name )
