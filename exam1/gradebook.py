"""gradebook.py: File with Python code solution
"""

__author__   = "Carolyn (Chih-Hsuan Kao)"
__version__  = "2.7.12"
__email__    = "chkao831@stanford.edu"
__date__     = "Oct 24,2019"

import math
import sys

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print('Usage:')
        print('python3 gradebook.py grades_file output_file m k [w_1...w_k]')
        sys.exit(0)
    elif len(sys.argv) > 5:
        count = len(sys.argv) - 5
        print(count)
        print(sys.argv[4])
        if (count != int(sys.argv[4])):
            print('the number of homework categories not match passed-in weights')
            sys.exit(0)
        else:
            weight = []
            for i in range(count):
                fl = float(sys.argv[5+i])
                if (fl>1 or fl<0):
                    raise ValueError("weight not within 0 and 1")
                weight.append(fl)
            if(math.isclose(sum(weight),1) == False):
                raise ValueError("weights not sum to one")
            inputfile = sys.argv[1]
            outputfile = sys.argv[2]
            numHW = int(sys.argv[3])
            numCate = int(sys.argv[4])
    else:
        numCate = int(sys.argv[4])
        weight = [float(1/numCate)]*numCate
        inputfile = sys.argv[1]
        outputfile = sys.argv[2]
        numHW = int(sys.argv[3])

def computeHWgrade(dicHW):
    """This function computes the minimum homework index and the value of
    the remaining weighted homework.
    Parameter: dicHW (dictionary)
    Returns: dicHWFinal (dictionary, key is id and value is hw score)
             dicHWMin (dictionary, key is id and value is minimum index)
    """
    dicHWFinal = {i:float(0) for i in list(dicHW.keys())}
    dicHWMin = {i:int(0) for i in list(dicHW.keys())}
    for sid in dicHW:
        #this list stores weighted score for each hw
        eachhw = []
        #for each homework
        for i in range(numHW):
            #current captures current weighted score
            current = 0
            for j in range(numCate):
                current += dicHW[sid][i*numCate+j]*weight[j]
            #after weighted for each homework, add to list
            eachhw.append(current)
        #now capture the lowest homework
        minimum_index = eachhw.index(min(eachhw))
        eachhw = [score for score in eachhw if score!=min(eachhw)]
        hwtotal = 0
        #after dropping, get weighted average
        for i in range(len(eachhw)):
            hwtotal += eachhw[i]
        hwtotal /= len(eachhw)
        #dicHWFinal has value of weighted hw
        dicHWFinal[sid] = hwtotal
        #dicHWMin has value of dropped
        dicHWMin[sid] = minimum_index
    return dicHWFinal, dicHWMin

def computeCombineGrade(dicHW):
    """This function computes the 50-50 weighted score of 
    combination of homework and exams
    Parameter: dicHW (dictionary) 
    Returns: dicTotal (dictionary, key is id value is combined score)
    """
    #this has id has key and floating number as value
    dicTotal = {i:float(0) for i in list(dicHW.keys())}
    #capture a dictionary of weighted hw
    dicHWFinal = computeHWgrade(dicHW)[0]
    for sid in dicTotal:
        hw = dicHWFinal.get(sid)
        exam = sum(dicExam[sid])/2
        dicTotal[sid] = (hw + exam)/2
    return dicTotal

dicHW = dict()
dicExam = dict()
f = open(inputfile)
for line in f:
    #dicHW is a dict with student id as key and all hw score list as value
    dicHW[line.split()[0]] = [float(x) for x in line.split()[1:-2]]
    #dicExam has id as key and exam score list as value
    dicExam[line.split()[0]] = [float(x) for x in line.split()[-2:]]
f.close()

#so far have: numHW, numCate, weight, inputfile, outputfile, dicHW, dicExam
#now call function to capture minimum index and grade
dicHWMin = computeHWgrade(dicHW)[1]
dicTotal = computeCombineGrade(dicHW)

#write to output file
f_write = open(outputfile,"w") 
#sort value in dictionary
for key,value in sorted(dicTotal.items(), key=lambda item:item[1], \
reverse = True):
    f_write.write(str(key))
    f_write.write(" ")
    f_write.write(str(dicHWMin[key]))
    f_write.write(" ")
    f_write.write("{:.3f}".format(dicTotal[key]))
    f_write.write(" ")
    f_write.write('\n')
