"""README.md: This is the text description of HW1 of CME211 Autumn19-20. HW1 has three parts. 
The first part is to create a small test case for further use in comparing with the output of program. 
The second part is about the file generatedata.py. This file accepts arguments regarding information including 
reference and reads and generates data according to the information. The third part is about the file processdata.py. 
It accepts one reference file and one read file, then write the alignment results to a new file, in which
each read is followed by the index/indices where it aligns. """

author = "Carolyn (Chih-Hsuan) Kao"
email  = "chkao831@stanford.edu"
date   = "Oct 3, 2019"


[PART 2] generatedata.py 
command line log demo:
$ python3 generatedata.py 1000 600 50 "ref_1.txt" "reads_1.txt" 
reference length: 1000
number reads: 600
read length: 50
aligns 0: 0.145
aligns 1: 0.7566666666666667
aligns 2: 0.09833333333333333

$ python3 generatedata.py 10000 6000 50 "ref_2.txt" "reads_2.txt" 
reference length: 10000
number reads: 6000
read length: 50
aligns 0: 0.15483333333333332
aligns 1: 0.743 
aligns 2: 0.10216666666666667

$ python3 generatedata.py 100000 60000 50 "ref_3.txt" "reads_3.txt" 
reference length: 100000
number reads: 60000 
read length: 50
aligns 0: 0.14616666666666667 
aligns 1: 0.7535333333333334
aligns 2: 0.1003

Describe in a paragraph in designing handwritten test data. If your code works properly for your handwritten data, 
will it always work correctly for others? 
My consideration in designing relatively small datasets did not 
involve a lot of techniques. I manipulated the reference string carefully such that the output is somehow 
consistent with the program description. I would say if my programs worked properly with my relatively small test
case, it guarantees nothing much since the test case might be so small in scale, and since it's written on my own, 
there might exist certain blind zone or edge cases that I failed to consider in testing out my program.

Should you expect an exact 15%/75%/10% distribution for the reads that align zero, one and two times? 
What other factors involve exactly? 
No, it's just an expectation, from the perspective of statistics. 
Firstly, the calculation in the program involves division, and the resulting number is a floating point,
so it's highly unlikely that it would be perfect integers. Secondly, since I separate the reference into different
quantiles, in such calculations, if the reference length is not divisible by 4, an error occurs when  I convert it 
to integer. 

How much time did you spend writing part 2? 
It took me more time reading and totally understand the instruction. 
Before start coding, it took me around (or more than) 1 hour to go through every requirement specified 
in the document. But the actual coding time was around 3-4 hours (including some format/syntax/debugging
issues since I haven't programmed in Python for a while and coding on vim editor on terminal wasn't very convenient).
The time mentioned above doesn't involve the time that I spent refining/further revising the code.

[PART 3] processdata.py
command line log demo:
$ python3 processdata.py ref_1.txt reads_1.txt align_1.txt 
reference length: 1000
number reads: 600
aligns 0: 0.145
aligns 1: 0.755 
aligns 2: 0.1 
elapsed time: 0.013927936553955078

$ python3 processdata.py ref_2.txt reads_2.txt align_2.txt 
reference length: 10000 
number reads: 6000
aligns 0: 0.15483333333333332 
aligns 1: 0.7428333333333333
aligns 2: 0.10233333333333333
elapsed time: 0.4007754325866699

$ python3 processdata.py ref_3.txt reads_3.txt align_3.txt
reference length: 100000
number reads: 60000
aligns 0: 0.14616666666666667 
aligns 1: 0.7535333333333334 
aligns 2: 0.1003
elapsed time: 36.423683881759644

Does this distribution of reads exactly match the output in part 2? 
It's very close, but not exactly. 
Again it involves floating point calculation. It also involves errors (about dividing the reference into different
quantiles) that I mentioned in part 2.

Using timing results to say about the scalability of implementation as the size of the reference and read length 
varies. 
At a coverge (=numReads*readLength/reference length) of 30, we could clearly see that the elapsed times 
greatly vary, depending on the reference length and num of reads. Suppose that we fix the read length to be 50, 
as we do in setting up our sample sizes. As illustrated, the human genome is approximately 3 billion base pairs. 
That is, in this calculation, we have 3 billion reads in parallel. 3,000,000,000 * 50 / 30 = 5,000,000,000. 
This yields a reference length of 5,000,000,000. Now I would like to perform a rough Big-O analysis. 
Take the refLength:numReads = 10000:6000 case for example. 
If we increase the size to refLength:numReads = 20000:12000, my program yields a result like 
reference length: 20000 
number reads: 12000
elapsed time: 1.5271575450897217
in contrast to the former 
length: 10000
number reads: 6000
elapsed time: 0.4007754325866699
We can see that as we double the size of numReads, the elapsed time 
approximately quadruple (precisely, 3.8105068847X). Hence, I would suggest that the algorithm is O(n^2). 
Back to the original problem. Given reference length and numReads above, 
3 billion reads = 6000 reads * 500,000
According to O(n^2), the runtime would be approximately 
0.4007754325866699 * (500,000)^2 = 100193858147 seconds = 1159651.1359606 days = 3175 years

Hence, based on such a computational system, it is not feasible to 
actually analyze all the data for a human using my program. 

How much time on writing this program? Less than part 2. Around 2 hours.

