This is the writeup for midterm 1

Name: Chih-Hsuan Kao (chkao831@stanford.edu)

I choose a procedural approach because it's more straightforward to me. 
The procedures like making containers sequentially by calling functions
simply consist of series of computational steps to be carried out. 
I acknowledge the fact that OOP, compared to my top down approach, is more 
secure and it is easy to add things or utilize later. 
If I had more time for this exam, I may build a Student class instead, 
as the bottom up approach gives more flexibility for further use. 

I split program into two functions, mainly for computations. 

I design my two test cases in a way that I could visualize my output and rank
them without actually doing math. 
The output in file 1 should rank like (student id)
235986723 0  
389769236 0 
2369872 1 
3762935 1 
489672 1

for file 2 should rank like
987236 1 
26389 2 
235698 2 
823690 3
69871 2 

And indeed my output to outputfile looks like that. 

This is how I dropped the lowest grade:
64         #now capture the lowest homework                                       
65         minimum_index = eachhw.index(min(eachhw))                              
66         eachhw = [score for score in eachhw if score!=min(eachhw)]        
And I suppose such complexity is O(n). Specifically, it takes average O(n) 
to find the minimum position (maybe less), then O(n) during list comprehension.
