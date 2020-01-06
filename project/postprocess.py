"""postprocess.py: This file generates pseudocolor plot with colorbar
of the temperature distribution within the pipe wall with isoline.
"""

__author__      = "Carolyn (Chih-Hsuan) Kao"
__version__     = "2.7.12"
__email__       = "chkao831@stanford.edu"
__date__        = "Dec 9, 2019"

from decimal import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import sys

if __name__ == "__main__":

    if (len(sys.argv)!=3):
        print('Usage:')
        print('  python3 {} <input file> <solution file>'.format(sys.argv[0]))
        sys.exit(0)
    inputfilename = sys.argv[1]
    outputfilename = sys.argv[2]
    print("Input file processed: {}".format(inputfilename))

    meantemp = 0.0
    term = 0.0
    count = 0
    matrixterm = []
    try:
        f = open(outputfilename)

        for line in f:
            term = (float)(line.split()[0])
            meantemp += term
            #read in file from lower left to upper right to list
            matrixterm.append(term)
            count += 1
        f.close()
    except IOError:
        raise IOError("Solution file not found with corresponding prefix.")

    meantemp = meantemp / count
    print("Mean Temperature: {}".format("{0:.5f}".format(meantemp)))

    length = 0.0
    width = 0.0
    h = 0.0
    try:
        f_input = open(inputfilename)
    
        for i,line in enumerate(f_input):
            if i==0:
                length = float(line.split()[0])
                width = float(line.split()[1])
                h = float(line.split()[2])
            else:
                pass
    except IOError:
        raise IOError("Inputfile not found.")

    x_step = int(length/h);
    y_step = int(width/h);
    #open soln file again and create numpy array
    f2 = open(outputfilename)
    npval_1d = np.loadtxt(f2)
    npval_2d = np.reshape(npval_1d,(y_step+1,x_step))
    f2.close()

    x_list = []
    y_list = []
    d = str(h)[::-1].find('.')
    #create x y indices
    nparr_x = np.around(np.linspace(h,length,x_step), decimals=int(d))
    nparr_y = np.around(np.linspace(0.0,width,y_step+1), decimals=int(d))  
    x_list = nparr_x.tolist()
    y_list = nparr_y.tolist()
    
    #for each column, get 1d interpolation
    interpolated_temporature = []
    for col in range(0,x_step):
        interpolated_temporature.append(np.interp(meantemp,npval_2d[:,col],y_list))

    #create nested dictionary: y coord as key; x coord as inner key; temperature as inner value
    dict_temp = dict((el,dict()) for el in y_list)
    #add to dictionaries
    position = 0
    for j in y_list:
        for i in x_list:
            dict_temp[j][i] = matrixterm[position]
            position += 1
    
    #use numpy meshgrid o create a rectangular grid out of two given one-dimensional
    #arrays representing the Cartesian indexing
    x = np.around(np.linspace(h,length,x_step), decimals=int(d)) 
    y = np.around(np.linspace(0.0,width,y_step+1), decimals=int(d))
    X,Y = np.meshgrid(x,y)

    @np.vectorize
    def val_func(x,y):
        return dict_temp[y][x]
    
    Z = val_func(X,Y)
    
    #plot and interpolate
    y_interpolate = np.array([])
    for val in interpolated_temporature:
        y_interpolate = np.append(y_interpolate, val)
    x_interpolate = np.around(np.linspace(0.0,length,x_step), decimals=int(d))  
    x_new = np.linspace(x_interpolate.min(),x_interpolate.max(),500)
    f = interpolate.interp1d(x_interpolate,y_interpolate,kind='cubic')
    y_smooth=f(x_new)
    image = plt.imshow(Z,cmap=plt.cm.jet,extent=(0.0,length,0.0,width),origin='lower')
    plt.colorbar(image)
    plt.plot(x_new,y_smooth,color='black')
    plt.savefig(outputfilename[0:-4])
    plt.show()

