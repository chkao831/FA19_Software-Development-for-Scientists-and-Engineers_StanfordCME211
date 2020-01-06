"""generatedata.py: This file accepts arguments from the command line
in the following order: the length of reference, the number of reads, 
the length of each read, the filename in which the reference is written,
the file name in which the reads are written. The primary functionality of 
this file is to create datasets with the information given by the user."""

__author__      = "Carolyn (Chih-Hsuan) Kao"
__version__     = "2.7.12"
__email__       = "chkao831@stanford.edu"
__date__        = "Oct 3, 2019"

import sys
import random
import copy

if __name__ == "__main__":
    #make sure the number of arguments from the command line is correct
    #note: for this assignment, I was that informed checking the validity of
    #each type of argument is not needed.
    if len(sys.argv) != 6:
        print("Usage:")
        print("$ python3 generatedata.py <ref_length> <nreads> " +
        "<read_len> <ref_file> <reads_file>")
        sys.exit(0)
    #otherwise, the input is valid. 
    #open the file where the reference would be written into
    f = open(sys.argv[4],"w")

    #generate a list that consists of four elements of genome data
    conversionList = ['A','T','C','G']

    #generate four numbers representing quantiles within the reference
    Quantile1 = int(int(sys.argv[1]) * 1/4) 
    Quantile2 = int(int(sys.argv[1]) * 1/2)
    Quantile3 = Quantile1 * 3
    Quantile4 = int(sys.argv[1]) #which is the total length of ref file
    #initialize an int variable to access the integer outcome for conversion
    #and initialize a string variable to represent the converted letter
    accessInt = 0
    convertedLetterIndex = ''

    #initialize a list of the first 75% of the randomly generated reference
    #and initialize a list of the last 25% which is copied from the last part
    first75 = []
    last25 = []
    #joinedNumList represents a list, consist of integers (non-converted data)
    #joinedLetterList represents a list of converted letters
    #joined_str is joinedLetterList in string format (also converted)
    joinedNumList = []
    joinedLetterList = []
    joined_str = ''

    #randomly generate the first 75% of the reference by assigning 4 different
    #integer outcomes and copy the last part of it to be the last 25% of ref    
    for i in range(Quantile3):
        first75.append(str(random.randint(0,3)))
    last25 = copy.deepcopy(first75[Quantile2:])
    joinedNumList = first75 + last25
   
    #perform conversion: for each element in the integer list, using
    #the conversion list (by index) to convert to letter
    for i in range(len(joinedNumList)):
        accessInt = joinedNumList[i]
        convertedLetterIndex = conversionList[int(accessInt)]
        joinedLetterList.append(convertedLetterIndex)
    joined_str = ''.join(joinedLetterList)
    #complete generating reference. Write to file and close the file. 
    f.write(joined_str)
    f.close()

    #start of generation of reads
    #firstly initialize integer variable numReads that represents num of reads
    #initialize int variable readLength that represents length of each read
    #open the file where the lines of reads would be written into        
    numReads = int(sys.argv[2])
    readLength = int(sys.argv[3])
    f_read = open(sys.argv[5],"w")
    
    #initialize integers variables to keep track of how many times
    #the new read actually aligns (zero, one or two, up to two). 
    aligns0 = 0
    aligns1 = 0
    aligns2 = 0

    #temp_read is a list that contains temporary read (letters) to be written
    #temp_read_str contains the string of read, each to be written as lines    
    for i in range(numReads):
        temp_read = []
        temp_read_str = ''
        #this random() returns a floating point value in the interval [0,1)
        #to achieve approximation of [0,0.75),[0.75,0.85),and [0.85,1)
        x = random.random()
        
        #with a 75% probability, generate reads that align once
        if x >= 0 and x < 0.75:
            #randomly pick a starting point in the first 50% of reference
            startPt = random.randint(0,Quantile2)    
            #for the ith read, generate the read according to readLength
            for j in range(readLength):
                temp_read.append(joined_str[startPt+j])
            temp_read_str = ''.join(temp_read)
            #increment actual number of alignment one to keep track
            aligns1 = aligns1 + 1
            f_read.write(temp_read_str + '\n')
        
        #with a 10% probability, generate reads that align twice            
        elif x >= 0.75 and x < 0.85:
            #randomly pick a starting point after the third quantile
            #but not too close to the end to avoid out of bound
            startPt = random.randint(Quantile3,Quantile4 - readLength)
            #for the ith read, generate the read according to readLength
            for j in range(readLength):
                temp_read.append(joined_str[startPt+j])
            temp_read_str = ''.join(temp_read)
            #increment actual number of alignment two to keep track
            aligns2 = aligns2 + 1
            f_read.write(temp_read_str + '\n')
        
        #with a 15% probability, generate reads that don't align
        else:
            #newRead is to temporarily record potential read
            #newReadListLetter temporarily holds converted read (list)
            #newReadStrLetter temporarily holds converted read (str)
            newRead = []
            newReadListLetter = []
            newReadStrLetter = ''

            #generate the read randomly according to readLength          
            for j in range(readLength):
                newRead.append(str(random.randint(0,3)))
            #perform conversion from integer to letter
            for j in range(len(newRead)):
                accessInt = newRead[j]
                convertedLetterIndex = conversionList[int(accessInt)]
                newReadListLetter.append(convertedLetterIndex)    
            newReadStrLetter = ''.join(newReadListLetter)
            #if the generated read is not found in reference, add it
            if (joined_str.find(newReadStrLetter) == -1):
                temp_newRead = ''.join(newReadListLetter)
                f_read.write(temp_newRead + '\n')
                #increment actual number of alignment zero to keep track
                aligns0 = aligns0 + 1
            #otherwise, the generated read already exists, repeat process
            else:
                continue
    
    print("reference length: {}".format(len(joinedNumList)))            
    print("number reads: {}".format(numReads))
    print("read length: {}".format(readLength))
    print("aligns 0: {}".format(aligns0/numReads))
    print("aligns 1: {}".format(aligns1/numReads))
    print("aligns 2: {}".format(aligns2/numReads))
    
