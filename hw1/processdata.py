"""processdata.py: This file accept from command line arguments, reading in
a reference file and a file that contains reads, and then write in an
alignment file whose name is specified by the last argument. 
The main purpose is to provide a certificate such that one can 
quickly examine each read, followed by location index(indices).
Note that in this program, for the sake of simplicity, if a read
appears more than twice, only cound up to the second alignment."""

__author__      = "Carolyn (Chih-Hsuan) Kao"
__version__     = "2.7.12"
__email__       = "chkao831@stanford.edu"
__date__        = "Oct 3, 2019"

import sys
import time

if __name__ == "__main__":
    if len(sys.argv) != 4: 
        print("Usage:")
        print("$ python3 processdata.py <ref_file> <reads_file> <align_file>")
        sys.exit(0)
        
#open the reference file and read it in (and strip the last whitespace)
with open(sys.argv[1], 'r') as ref:
	f_ref = ref.read()
	f_ref = f_ref.strip() 
ref.close()
#create a list to store each read
readList = []
#open the read file and read it in (and strip each empty line btw reads)
with open(sys.argv[2], 'r') as f_read:
	for line in f_read:
		line = line.strip()
		readList.append(line)
f_read.close()

#open the alignment file to write
f_write = open(sys.argv[3], "w") 
#initialize integer variables to keep track of actual alignments
aligns0 = 0
aligns1 = 0
aligns2 = 0
#before the start of actual alignment, record time
start = time.time()

#the outer loop is for iteration of each read
for i in range(len(readList)):
	#create integer variables to record if a certain read 
	#has first alignment, and then if it has second one after that
	firstTime = 0
	secondTime = 0
	#firstly, upon reading in a read, write to file
	f_write.write(str(readList[i]))

	#for inner loop is for finding read recursively
	for j in range(len(f_ref)):
	    #if there is no first alignment (i.e. no alignment at all)
		if(f_ref.find(readList[i],j,len(f_ref)) == -1):
		    #write in -1 and increment count
			f_write.write(' '+'-1'+'\n')		
			aligns0 = aligns0 + 1
			break
		#otherwise, if there is first alignment BUT no second one
		elif(f_ref.find(readList[i],
		(f_ref.find(readList[i],j,len(f_ref)))+1,len(f_ref)) == -1):
			firstTime = f_ref.find(readList[i],j,len(f_ref))
			#capture its index and write to file &  increment count
			f_write.write(' '+str(firstTime)+'\n')
			aligns1 = aligns1 + 1
			break
		#otherwise, if there is first alignment AND second one
		else:
		    #firstly capture its index of first appearance
		    #then capture its index of second appearance, write both
			firstTime = f_ref.find(readList[i],j,len(f_ref)) 
			secondTime = f_ref.find(readList[i],firstTime+1,len(f_ref))
			f_write.write(' '+str(firstTime)+' '+str(secondTime)+'\n')
			#increment count
			aligns2 = aligns2 + 1
			break	
#close the alignment file
f_write.close()
#by the end of actual alignment, record time
end = time.time()

print("reference length: " + str(len(f_ref)))
print("number reads: " + str(len(readList)))
print("aligns 0: " + str(aligns0/len(readList)))
print("aligns 1: " + str(aligns1/len(readList)))
print("aligns 2: " + str(aligns2/len(readList)))
print("elapsed time: " + str(end-start))
