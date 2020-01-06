"""bonus.py: This file generates animation of
temperature distribution during CG for every 10 iteration.
"""

__author__      = "Carolyn (Chih-Hsuan) Kao"
__version__     = "2.7.12"
__email__       = "chkao831@stanford.edu"
__date__        = "Dec 9, 2019"

import matplotlib
matplotlib.use('Agg')
import matplotlib.image as mgimg
import matplotlib.pyplot as plt
from matplotlib import animation
import os
import postprocess
import subprocess
import sys


if len(sys.argv) != 3:
    print('Please make sure solution txt files corresponding to the input txt file \
are generated in the directory before usage.')
    print('Usage:')
    print('  python3 {} <inputfile> <soln_prefix>'.format(sys.argv[0]))
    print('Example:')
    print('  python3 bonus.py input2.txt output')
    sys.exit(0)

fig = plt.figure()

#get inputfile number and append with solution prefix
inputfile=sys.argv[1]
numstr = inputfile[5:-4]
outputnum = sys.argv[2] + numstr
unsorted_textfiles = (fn for fn in os.listdir('.') if (fn.startswith(outputnum) and fn.endswith('.txt')))
unsorted_text_list = list(unsorted_textfiles)

#solution file not found
if len(unsorted_text_list) == 0:
    print('There does not exist solution txt files corresponding to the inputfile and soln prefix.')
    print('Please make and run ./main <inputfile> <soln_prefix> before usage.')
    print('Example: $make')
    print('         $./main input2.txt output')
    print('         $python3 bonus.py input2.txt output')
    sys.exit(0)

#run postprocess.py for txt file
for ele in unsorted_text_list:
    pre = "python3 postprocess.py"
    middle = inputfile
    callstring = ele
    finalstring = pre + " " + middle + " " + ele
    subprocess.call(finalstring,shell=True)

#now png files are there, sort and get maximum convergence
unsorted_filenames = (fn for fn in os.listdir('.') if (fn.startswith(outputnum) and fn.endswith('.png')))
unsorted = list(unsorted_filenames)
maxnum = -1
curstr = ''
curnum = 0;
for ele in unsorted:
    curstr = ele.split("_")[1]
    curstr = curstr.split(".")[0]
    curnum = int(curstr)
    if(curnum > maxnum):
        maxnum = curnum

myimages = []

#loops through available png
for p in range(1,maxnum+1):

    # Read in picture
    if(p==1 or p%10==0 or p==maxnum):
        fnamestr = outputnum + "_%d.png"
        fname = fnamestr %p 

        img = mgimg.imread(fname)
        imgplot = plt.imshow(img)

        # append AxesImage object to the list
        myimages.append([imgplot])

# create an instance of animation
my_anim = animation.ArtistAnimation(fig, myimages, interval=1000, blit=True, repeat_delay=1000)

plt.show()
