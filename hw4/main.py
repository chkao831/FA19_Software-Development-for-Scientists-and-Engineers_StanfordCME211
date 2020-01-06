"""main.py: This file executes the program truss.py from the command line. 
The initialization of this class takes arguments the names for joints and 
beams file, and an optional output graph filename. 
"""

__author__      = "Carolyn (Chih-Hsuan) Kao"
__version__     = "2.7.12"
__email__       = "chkao831@stanford.edu"
__date__        = "Oct 31, 2019"

import sys
import truss

#if the number of arguments are not 3 or 4, print usage message
if ((len(sys.argv) < 3) or (len(sys.argv) >4)):
    print('Usage:')
    print('  python3 {} [joints file] [beams file] \
[optional plot output file]'.format(sys.argv[0]))
    sys.exit(0)

#otherwise, can perform task
inputbeam = sys.argv[2]
inputjoint = sys.argv[1]
#if optional output file name is given, passed-in
if len(sys.argv) == 4:
    outputfile = sys.argv[3]
#if not, pass in an empty string
else:
    outputfile = ''
obj = truss.Truss(inputbeam, inputjoint, outputfile)
print(obj)
