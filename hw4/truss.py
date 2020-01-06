"""truss.py: This file contains class Truss. The class Truss performs analysis
of the stability and forces in a 2D truss using the method of joints. 
"""
__author__      = "Carolyn (Chih-Hsuan) Kao"
__version__     = "2.7.12"
__email__       = "chkao831@stanford.edu"
__date__        = "Oct 31, 2019"

import math
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import coo_matrix

class Truss:
    """Truss class gathers information about a 2D truss at a time, from two 
    files which contain information of joints (number, xycoord., force in xy
    direction, a boolean indicating whether it has fixed support) and contain
    information of beams (number and joints on each side). Then, using method
    of joints, the class is capable of plotting a simple 2D plot showing 
    the geometry of the truss as well as calculating beam forces for the truss
    and print out (to file if an optional command of output filename is given).
    """

    def __init__(self,inputbeam, inputjoint,outputfile):
        """This serves as a constructor in OOP Design.
        It initializes attributes of class Truss and and takes care of
        general tasks that are related to the functionality of this class.
        
        Parameters
        ----------
        inputbeam: file
            This is a beam file that contains beam information
        inputjoint: file
            This is a joint file that contains joint information
        outputfile: string
            This is a string that specifies the name of output filename
        """

        #load data to numpy
        self.__beams = np.loadtxt(inputbeam, dtype = "int")
        self.__joints = np.loadtxt(inputjoint)
        if(outputfile!=''):
            self.PlotGeometry(outputfile)
        #these three lists capture information to be passed into sparse matrix
        self.__value = list()
        self.__col = list()
        self.__row = list()
        #dictionaries with jointnum as key and x/y coordinate as value
        self.__dictX = self.CreateJointDict()[0]
        self.__dictY = self.CreateJointDict()[1]    
        self.CalculateReactionForce()
        self.CalculateBeamForce()
        #list comprehension and create matrix
        self.__row = [int(i) for i in self.__row]
        self.__col = [int(i) for i in self.__col]
        nprow = np.array(self.__row)
        npcol = np.array(self.__col)
        npval = np.array(self.__value)
        self.__matrix = coo_matrix((npval,(nprow,npcol)))
        #performs linear algebra matrix solving using function from numpy
        try:
            A = self.__matrix.todense()
            #b is the external force, given from joint file
            list_b = []
            for i in range(len(self.__joints)):
                list_b.append(-(self.__joints[i][3]))
                list_b.append(-(self.__joints[i][4]))
            np_b = np.array(list_b)
            x = np.linalg.solve(A,np_b)
            self.__solution = x
        #exception handling if A is singular or if A is non-square
        except np.linalg.linalg.LinAlgError as err:
            if 'Singular matrix' in str(err):
                raise RuntimeError("Cannot solve the linear system, \
unstable truss?") from None
            elif 'Last 2 dimensions of the array must be square' in str(err):
                raise RuntimeError("Truss geometry not suitable for \
static equilibrium analysis") from None

    def PlotGeometry(self,outputfile):
        """This method plots graph showing the geometry of the truss
        if an optional outputfile name is given in the command line. 
        If given name, a plot would be written to the specified filename.
        
        Parameters
        ----------
        outputfile: string
            This string specifies the outputfile name to which the plot
            is written. 
        """

        #read in every line from the beam file and plot beam by joints
        #that are located on each side of the beam
        for i in range(len(self.__beams)):
            first_joint = self.__beams[i][1]
            second_joint = self.__beams[i][2]
            x_first = self.__joints[first_joint-1][1]
            y_first = self.__joints[first_joint-1][2]
            x_second = self.__joints[second_joint-1][1]
            y_second = self.__joints[second_joint-1][2]
            plt.plot([x_first,x_second],[y_first,y_second],\
                    color='m',linewidth=7.0)
        plt.savefig(outputfile)

    def CreateJointDict(self):
        """This method returns two dictionaries, in which the number of 
        each joints is key, and its x or y coordinates are values. 
        This method is created for computational usage (part of decomposition)
        
        Returns
        -------
        dict_x: dictionary
            This is a dictionary that has joint number as key and its 
            x coordinate as value
        dict_y: dictionary
            This is a dictionary that has joint number as key and its 
            y coordinate as value
        """

        list_key = list()
        list_x = list()
        list_y = list()
        dict_x = dict()
        dict_y = dict()
        #read in each line (each joint) from joint file
        for i in range(len(self.__joints)):
            list_key.append(self.__joints[i][0])
            list_x.append(self.__joints[i][1])
            list_y.append(self.__joints[i][2]) 
        dict_x = dict(zip(list_key,list_x))
        dict_y = dict(zip(list_key,list_y))
        return dict_x, dict_y

    def CalculateBeamForce(self):
        """This method performs main task of this class. Iterating through
        each beam, it computes the beam force for 4 entries at each iteration, 
        regarding the value of the entry, the row location, the column location.
        Those information would be appended to three lists respectively for
        further usage of COO matrix creation. 
        """
        
        deltaX = 0
        deltaY = 0
        beamlens = 0
        valueX = 0
        valueY = 0
        #for each beam (each column)
        for i in range(len(self.__beams)):
            key_beam = self.__beams[i][0]
            joint_A = self.__beams[i][1]
            joint_B = self.__beams[i][2]
            #calculate beam length
            beamlen=math.sqrt((self.__dictX[joint_A]-self.__dictX[joint_B])**2\
                    + (self.__dictY[joint_A] - self.__dictY[joint_B])**2)
            deltaX = -(self.__dictX[joint_B] - self.__dictX[joint_A])
            deltaY = -(self.__dictY[joint_B] - self.__dictY[joint_A])
            #X dir, for jointA
            valueX = deltaX / beamlen
            self.__value.append(valueX)
            self.__col.append(key_beam - 1)
            self.__row.append(joint_A*2-2)
            #Y dir, for jointA
            valueY = deltaY / beamlen
            self.__value.append(valueY)
            self.__col.append(key_beam - 1)
            self.__row.append(joint_A*2-1)
            #X dir, for jointB
            self.__value.append(-(valueX))
            self.__col.append(key_beam - 1)
            self.__row.append(joint_B*2-2)
            #Y dir, for jointB
            self.__value.append(-(valueY))
            self.__col.append(key_beam - 1)
            self.__row.append(joint_B*2-1)
    
    def CalculateReactionForce(self):
        """This method handles the last few columns of the matrix. In those 
        columns, reaction force would present if fixed support is there. 
        Firstly, the method would check if a joint has fixed support, if so, 
        the joint number would be saved to a set. 
        """
        
        #This set stores the number of joint that has fixed support
        setBooleanTrue = set()
        for i in range(len(self.__joints)):
            if(self.__joints[i][5]==1):
                setBooleanTrue.add(self.__joints[i][0])
            else:
                pass
        #now the set contains the jointnum with boolean true
        #this variable keeps track of col location of current reaction force
        currentcol = len(self.__beams)-1
        for key in setBooleanTrue:
            currentcol += 1
            self.__value.append(1.0)
            self.__row.append(key*2-2)
            self.__col.append(float(currentcol))
            currentcol += 1
            self.__value.append(1.0)
            self.__row.append(key*2-1)
            self.__col.append(float(currentcol))
    
    def __repr__(self):
        """This overloads representation method of the class Truss. 
        When printing out Truss object, the representation string would 
        be printed out to the command line. 

        Returns
        -------
        str: string
            This string contains the information to be printed to command line.
        """

        str = ''
        str += ('Beam       Force')
        str += ("\n")
        str += ('-----------------')
        str += ("\n")    
        for i in range(len(self.__beams)):
            sol = "{0:9.3f}".format(self.__solution[i])
            str += ("{}".format(self.__beams[i][0])+ '      '+sol)
            str += ("\n")    
        return str
