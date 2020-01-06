"""airfoil.py: This file is a Python module containing Airfoil class definition.
"""

__author__      = "Carolyn (Chih-Hsuan) Kao"
__version__     = "2.7.12"
__email__       = "chkao831@stanford.edu"
__date__        = "Oct 12, 2019"

import glob
import math
import os
import sys

class Airfoil:
    """Airfoil class gathers information about the computational fluid 
    such as pressure coefficient, chord length of the airfoil geometry,
    correponding x,y of alpha value, etc. Then it computes Cartesian directions
    in each direction, non-dimensional force component perpendicular to the 
    flow direction and so on, and prints out results to the command line.
    """
    
    def __init__(self,inputdir):
        """This serves as a constructor in OOP Design.
        It initializes attributes of class Airfoil and takes care of
        general tasks that are related to the functionality of this class.
        """

        #attributes initialization
        self.__inputdir = input
        self.__lead_x = 0
        self.__lead_y = 0
        self.__trailing_x = 0
        self.__trailing_y = 0
        self.__totalfile = []
        self.__dictdata = dict()
        print("Test case: {}".format(inputdir))
        try:
        #get the path of directory
            path = os.path.abspath(inputdir)
        except:
            raise OSError("inputdir not exists") 
        #get a list of all file in directory
        totalfile = glob.glob1(path, '*.dat')
        #separate xy data file from the list
        #such that list only contains alpha data
        #handle error case in case xy.dat does not exist
        try:
            totalfile.remove('xy.dat')
        except:
            raise OSError("xy data file not exists")
        self.__totalfile = totalfile
        #initiate a list that contains alpha value (int)
        list_num = list()
        for index, alphadata in enumerate(self.__totalfile):
            item = alphadata[5:-6]
            if item[0] == '+':
                item = int(item[1:])
            elif item[0] == '-':
                item = int(item)
            else:
                item = int(item[0])
            list_num.append(item)
        #initiate a dictionary that has key as alpha value (int)
        #and correponding file path as value
        for i in range(len(list_num)):
            key = list_num[i]
            self.__dictdata[key]=os.path.join(inputdir,totalfile[i])
        #get the path of xy file directory
        xyfile = os.path.join(inputdir,'xy.dat')
        self.__xy = xyfile
        f = open(xyfile,'r')
        self.__chord = self.get_chord()
        #construct dictionary in which alpha value is key
        #and cl value is value
        self.__cl = dict(zip(list(self.__dictdata.keys()), \
        self.get_cl()))
        #construct dictionary in which alpha value is key
        #and stagnation point in x dir is value
        self.__stag_x = dict(zip(list(self.__dictdata.keys()), \
        self.get_stag()[0]))
        #construct dictionary in which alpha value is key
        #and stagnation point in y dir is value
        self.__stag_y = dict(zip(list(self.__dictdata.keys()), \
        self.get_stag()[1]))
        #construct dictionary in which alpha value is key
        #and stagnation coefficient is value
        self.__stag_coeff = dict(zip(list(self.__dictdata.keys()), \
        self.get_stag()[2]))
        #print string representation to command line
        self.print()
        
    def get_chord(self):
        """The functionality of this method is to get the length of
        chord.
        """

        f = open(self.__xy,'r')
        diff = 0
        for i,line in enumerate(f):
            if i==0:
                pass
            else:
                #get trailing x and y at the beginning
                if i==1:
                    self.__trailing_x = float(line.split()[0])
                    self.__trailing_y = float(line.split()[1])
                #iterate, get the biggest difference in x and capture it
                if (self.__trailing_x - float(line.split()[0]) > diff):
                    diff = self.__trailing_x - float(line.split()[0])
                    self.__lead_x = float(line.split()[0])
                    self.__lead_y = float(line.split()[1])
        x_dis_squared = (self.__trailing_x - self.__lead_x)**2
        y_dis_squared = (self.__trailing_y - self.__lead_y)**2
        chord = (math.sqrt(x_dis_squared + y_dis_squared))
        return chord

    def get_c(self, filename):
        """The functionality of this method is to compute delta_cx
        and delta_cy, and then match each of them with the pressure
        coefficient. Lastly, summing them up yields cx and cy. 
        It also simultaneously computes the information about the 
        stagnation points.
        """

        f1 = open(filename, 'r')
        f2 = open(self.__xy, 'r')
        #initialize x and y (lists) to store value from col x and y
        x = []
        y = []
        for i, line in enumerate(f2):
            if i == 0:
                pass
            else:
                x.append(float(line.split()[0]))
                y.append(float(line.split()[1]))
        #get delta for each direction 
        delta_x = [a - b for a, b in zip(x[1:], x[:-1])]
        delta_y = [a - b for a, b in zip(y[1:], y[:-1])]
        #divided by chord and adjust sign (according to formula)
        delta_cx = [-(i/self.__chord) for i in delta_y]
        delta_cy = [i/self.__chord for i in delta_x]
        #Keeps track of the current difference 
        #between 1 and current stagnation point
        min_diff = 1
        minimum_str = ""
        minimum_index = 0
        #initialize average variables to for return of stagnation
        average_x = 0
        average_y = 0
        #loop through every line
        for i, line in enumerate(f1):
            if i == 0:
                pass
            else:
                temp = float(line.split()[0])
                #update and keep track of stagnation point
                if (abs(temp-1) < min_diff):
                    min_diff = abs(temp-1)
                    minimum_str = float(line)
                    minimum_index = i
                #multiplied by pressure coefficient
                delta_cx[i-1] = delta_cx[i-1] * temp
                delta_cy[i-1] = delta_cy[i-1] * temp
        cx = sum(delta_cx)
        cy = sum(delta_cy)
        average_x = (x[minimum_index-1]+x[minimum_index])/2
        average_y = (y[minimum_index-1]+y[minimum_index])/2
        return cx, cy, minimum_str, average_x, average_y

    def get_cl(self):
        """This method computes the lift coefficient. 
        """
        
        #Handle error when we have trouble reading file
        try:
            cx = [self.get_c(file)[0] for file in \
            list(self.__dictdata.values())]
            cy = [self.get_c(file)[1] for file in \
            list(self.__dictdata.values())]
        except:
            raise IOError("trouble reading in data")
        alpha = list(self.__dictdata.keys())
        cl = []
        for i in range(len(alpha)):
            cl.append(cy[i]*math.cos(math.radians(alpha[i]))- \
            cx[i]*math.sin(math.radians(alpha[i])))
        return cl

    def get_stag(self):
        """This method calls get_c and captures some of the 
        information it returns, including the x&y coordinates of
        stagnation point and the coefficient.
        It ultimately returns x,y,coefficient in list respecrtively.
        """
        
        x = []
        y = []
        coeff = []
        x = [self.get_c(file)[3] for file in \
        list(self.__dictdata.values())]
        y = [self.get_c(file)[4] for file in \
        list(self.__dictdata.values())]
        coeff = [self.get_c(file)[2] for file in \
        list(self.__dictdata.values())]
        return [x,y,coeff]

    def print(self):
        """This method prints out information to command line.
        It overwrites the string representation method.
        """
        
        print('alpha     cl           stagnation pt')
        print('-----   -------   --------------------------')
        alpha = sorted(list(self.__dictdata.keys()))
        for i in range(len(alpha)):
            if alpha[i] >= 0:
                a = ' ' + str(round(alpha[i],2))+ '.00'
            else:
                a = str(round(alpha[i],2)) + '.00'
            if self.__cl[alpha[i]] >= 0:
                c = ' ' + "{0:.4f}".format(self.__cl[alpha[i]])
            else:
                c = "{0:.4f}".format(self.__cl[alpha[i]])
            if self.__stag_y[alpha[i]]>=0:
                s = "{0:.4f}".format(self.__stag_x[alpha[i]]) + \
                ',  ' + "{0:.4f}".format(self.__stag_y[alpha[i]])
            else:
                s = "{0:.4f}".format(self.__stag_x[alpha[i]]) + \
                ', ' + "{0:.4f}".format(self.__stag_y[alpha[i]])
            print(a + '   ' + c + '   ' + '(' + s + ')' + \
            '   ' + "{0:.4f}".format(self.__stag_coeff[alpha[i]]))
