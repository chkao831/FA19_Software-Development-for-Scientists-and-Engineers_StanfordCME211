"""README.txt: This is the text description of HW2 of CME211 Autumn19-20."""

author = "Carolyn (Chih-Hsuan) Kao"
email  = "chkao831@stanford.edu"
date   = "Oct 9, 2019"

[Part 1]
1. What were your considerations when creating this test data?
    My considerations include but not limited to
        -There might be larger gaps between integers (not consecutive integers).
        -There might be more than one whitespace between each value.
        -Not every user rates all 3 movies. (Could do only 1 or 2). 
        -Some users are more extreme (tend to give 1 or 5) yet some users are
        more neutral (tend to give between 2 to 4). 
        -The value of m (the number of users that have rated both two movies)
        does not stay the same for every pair. 
        -Unlike MovieLens data, not all id's are natural number. (some negative)
        -The order of corresponding user and movie tends to be random (I
        tried to make the order appears to be as random as possible)

2. Were there certain characteristics of the real data and file format that 
you made sure to capture in your test data?
    -In the real (MovieLens) data, there occasionally exists more whitespaces 
    between each values in a line. Mostly it is just one whitespace, but sometimes
    becomes two, three to some tabs. I made sure to reflect this in mine. 
    -The ordering of each line seems to be random among the data file. 

3. Did you create a reference solution for your test data? If so, how?
    Yes. I have a rough assumption upon completing the test data. 
    When constructing the test case, I tried to make movies with id's
    '72' and '540' as positive correlated, while making these two negatively
    correlated with movie id '-3'. That is, users usually tend to prefer
    '72' and '540' at the same time while dislike '-3', or oppositely they
    tend to prefer '-3' while giving '72' and '540' lower rates. 
    Hence, I ideallly assume that P (cosine similarity) between movie with
    id '72' and '540' to be positive; between '72' and '-3' to be negative; 
    between '540' and '-3' to be negative. 

[Part 2]
1. In your HW2 README file, include a command line log of using your program 
to compute similarities on the ml-100k/u.data data file.

    Input MovieLens file: ml-100k/u.data
    Output file for similarity data: similarities.txt
    Minimum number of common users: 5
    Read 100000 lines with total of 1682 movies and 943 users
    Computed similarities in 30.382341146469116 seconds

Also include the first 10 lines of the output similarity file.

    1 (918,0.9105046586065211,5)
    2 (1056,0.9999805766784162,5)
    3 (1081,0.9770523936627928,5)
    4 (35,0.8035001899406667,6)
    5 (976,0.9330795632032152,5)
    6 (279,0.9597565073371667,5)
    7 (968,0.997420592235218,7)
    8 (590,0.8646937307646155,6)
    9 (113,0.9644943052520142,5)
    10 (1202,0.9724294104431035,5)

2. Also, in your HW2 README briefly explain in no more than one paragraph
the decomposition of your program in terms of functions.

   I have four functions in the program. The 1st function is called 
   createdictionaries, which creates 4 dictionaries that represents 
   {movie:userid},{user:{movie:rate}},{movie:averagerate},{movie:usercount}
   respectively. The 2nd function is called createset, which counts the 
   number of total lines in the input data and creates a set of movie id's
   and a set of movie users. The 3rd function is called getcorrelation. 
   Its functionality is to compute the correlation, given two movie id's.
   The 4th function is called parallel_lists, which creates four parallel 
   lists that respectively contain distinct movie id's, the currently
   largest correlation that each movie corresponds to, the currently
   most-correlated movie, and the current count of common users
   between a movie and the most-correlated one.
