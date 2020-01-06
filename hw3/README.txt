"""README.txt: This is the text description of HW3 of CME211 Autumn19-20."""

author = "Carolyn (Chih-Hsuan) Kao"
email  = "chkao831@stanford.edu"
date   = "Oct 14, 2019"

Question: 
-Provide Explanation of Code Design
    include OOP abstraction, decomposition, and encapsulation
-Error Checking and Exception Handling

Answer:

In the class Airfoil, I divided the whole class into 6 methods:
__init__: the constructor that initializes attributes of the class
          and performs general tasks
get_chord: a method that returns the legnth of the chord
get_c: a method that takes in the filename of alphadata file and then
       returns related information including cx, cy, the stagnation point
       as a float, and the x and y coordinates of the stagnation point
get_cl: a method that computes the lift coefficient and returns it
get_stag: a method that provides the information regarding stagnation points
print: it overwrites the initial string representation method and prints
       things to command line

I don't create abstraction in this class other than AirFoil objects. 

Most attributes in this class are private ones, such that they are accessed
from within its own class. I only define the init as private method. 
The attributes I created for general usage include (but not limited to)
self.__inputdir that stores path
self.__lead_x that stores x coordinate of leading edge (similarly to y)
self.__trailing_x that stores x coord of trailing edge (similarly to y)
self.__totalfile is a list that stores strings of alpha data file name
self.__dictdata is a dictionary that has key has alpha and data path as value
self.__xy that stores the path of xy file
self.__cl is a dictionary with alpha as key, cl as value
self.__stag_x is a dictionary. Key is alpha, stag x coord as value (similarly 
to y)
self.__stag_coeff is a dictionary with alpha as key and stagnation coefficient
as value.

I did several error checking 
like ensuring that xy.dat file exists
raising exception with there is trouble reading in data
raising exception when input directory does not exist

