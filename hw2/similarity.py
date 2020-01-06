"""similarity.py: This file writes a Python program to find for each movie the
one other movie that is most similar (i.e. similarity coefficient closest to
1.0). It takes in command line arguments as the followings: name of input data,
name of output file in which similarity information is written, and an optional
threshold that represents the minimum number of common users between two."""

__author__      = "Carolyn (Chih-Hsuan) Kao"
__version__     = "2.7.12"
__email__       = "chkao831@stanford.edu"
__date__        = "Oct 7, 2019"

#modules should be imported in alphabetic order
import math
import sys
import time

#A magic number that would later be used for input of invalid correlation
#such that value wouldn't be updated in cases where it shouldn't be
NEGATIVE = -100
#A magic number for the initial correlation value
#such that when passing in a valid correlation, correlation is updated
NEGATIVE_CORR = -2

def createdictionaries(movie,user,inputfile):
    """Creates 4 dictionaries that represents {movie:userid},
    {user:{movie:rate}},{movie:averagerate},{movie:usercount}.

    Parameters
    ----------
    movie : set
        A set of movie id
    user : set
        A set of movie user
    inputfile : file
        An input file in which movie user, id and rate are contained

    Returns
    -------
    dic_mv : dictionary
        A dictionary whose key is movie id, value is user id
    dic_usr : dictionary (nested dictionary)
        A dictionary whose key is user id, value is another dictionary.
        In the nested dictionary, the key is movie id, value is rating
    dic_rate : dictionary
        A dictionary whose key is movie, value is average rating given
        by all of its viewers
    dic_count : dictionary
        A dictionary whose key is movie, value is total count of user
    """

    #generate a dictionary with movie as key, a set of users as value
    dic_mv = {i: set() for i in movie}
    #generate a nested dictionary with user ID as key
    #and dictionary as value, in which movie ID is key and rate is value
    dic_usr = {i: dict() for i in user}
    dic_rate = dict( (eleSetMovie,int(0)) for eleSetMovie in movie)
    dic_count = dict( (eleSetMovie,int(0)) for eleSetMovie in movie)
    #open and read in data from file
    f = open(inputfile)
    for line in f:
        dic_mv[line.split()[1]].add(line.split()[0])
        dic_usr[line.split()[0]][line.split()[1]] = line.split()[2]
        #get the rate from the movie of the line and increment
        x = dic_rate.get(line.split()[1])
        x += int(line.split()[2])
        dic_rate[line.split()[1]] = x
        #increment the user count from the movie of the line
        y = dic_count.get(line.split()[1])
        y += 1
        dic_count[line.split()[1]] = y
    f.close()
    #calculate average rate for each movie
    for item in dic_rate:
        sum = dic_rate[item]
        sum = sum/dic_count[item]
        dic_rate[item] = sum
    return dic_mv,dic_usr,dic_rate,dic_count

def createset(inputfile):
    """Creates 2 sets and count the number of total lines in the data.
    The two sets are a set of movie id's and a set of movie users.

    Parameters
    ----------
    inputfile : file
        An input file in which movie user, id and rate are contained

    Returns
    -------
    movie : set
        A set of distinct movie id's
    user : set
        A set of distinct users
    count : int
        An integer that represents total read-in lines from inputfile
    """

    movie = set()
    user = set()
    count = 0
    #open and read in data from file
    f = open(inputfile)
    for line in f:
        #adding all unique keys to setMovie
        movie.add(line.split()[1])
        #adding all unique users to setUser
        user.add(line.split()[0])
        count+=1
    f.close()
    return movie,user,count

def getcorrelation(movieid1,movieid2):
    """Computes the correlation, given two movie id's.

    Parameters
    ----------
    movieid1 : str
        The first passed-in movie for which the correlation is calculated
    movieid2 : str
        The second passed-in movie for which the correlation is calculated

    Return
    -----
    correlation : int
        The correlation between the two movies
    """

    #the initialized integer, cosine_sum, has an initialized value of -100
    #such that in the case where correlation shouldn't be updated, the value
    #remains unchanged
    cosine_sum = NEGATIVE
    #variable r_a,i and r_b,i in the formula
    r_mv1 = 0
    r_mv2 = 0
    #numerator
    nume_sum = 0
    #two parts in the denominator (before taking square root)
    deno_mv1_sum = 0
    deno_mv2_sum = 0
    denominator = 0
    #variable that keeps track of count of common users
    currentCommon = 0

    #firstly check if the count of user passes the threshold for each movie
    if(len(dictMovie.get(movieid1))<threshold or
    len(dictMovie.get(movieid2))<threshold):
        #if either does not, returns a negative correlation (to be invalid)
        return cosine_sum
    #if both pass threshold, get the intersection (of users) of two movies
    else:
        intersect=dictMovie.get(movieid1).intersection(dictMovie.get(movieid2))
        #if the number of common users is smaller than threshold, return
        if (len(intersect) < threshold):
            return cosine_sum
        #otherwise, start counting correlation
        else:
            #get the average rating of two movies
            mv1_bar = float(dictMovieRate.get(movieid1))
            mv2_bar = float(dictMovieRate.get(movieid2))
            #iterate through common users and use formula
            for commonuser in intersect:
                #increment common user count
                currentCommon += 1
                r_mv1 = int(dictUser.get(commonuser).get(movieid1))
                r_mv2 = int(dictUser.get(commonuser).get(movieid2))
                nume_sum += ( (r_mv1)-mv1_bar )*( (r_mv2)-mv2_bar )
                deno_mv1_sum += ( (r_mv1)-mv1_bar )**2
                deno_mv2_sum += ( (r_mv2)-mv2_bar )**2
            #when done with denominator separate calculation, combine
            denominator = math.sqrt(deno_mv1_sum * deno_mv2_sum)
            #handle the case where denominator=0 (invalid)
            if denominator == 0:
                return cosine_sum
            #otherwise, successful. return valid values and pass in
            #common count to global variable for program to catch
            else:
                cosine_sum = nume_sum / denominator
                global currentCommonCount
                currentCommonCount = currentCommon
                return cosine_sum

def parallel_lists(movie):
    """Creates four lists in which data are paralleled correponding to indices.
    The 4 lists contain distinct movie id's, the currently largest correlation
    that each movie corresponds to, the currently most-correlated movie, and
    the current count of common users btw a movie and the most-correlated one.

    Parameters
    ----------
    movie : set
        A set of movie id

    Returns
    -------
    mv : list
        A list of distinct movies
    currentMax : list
        A list of the corresponding movie's currently largest correlation
    currentMatch : list
        A list of the corresponding movie's currently mostly correlated movie
    currentCommon: list
        A list of the corresponding movie's current count of common users
        between it and the currently most-correlated movie
    """

    mv = []
    #pass in the distinct movie id and sort by the order of integer value
    for eleMovieSet in movie:
        mv.append(eleMovieSet)
    mv.sort(key=int)
    #initialize a list of current max with negative two inside such that
    #it's guaranteed that when passing in a valid correlation, it's updated
    currentMax = [NEGATIVE_CORR]*(len(mv))
    #initialize lists of current match and current common with None
    currentMatch = [None]*(len(mv))
    currentCommon = [None]*(len(mv))
    return mv,currentMax,currentMatch,currentCommon

if __name__ == "__main__":
    #make sure the number of arguments from the command line is correct
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage:")
        print("$ python3 similarity.py <data_file> <output_file>" +
        "[user_thresh (default = 5)]")
        sys.exit(0)
    if len(sys.argv) == 4:
        threshold = int(sys.argv[3])
    #if the threshold is not specified, set to default value of 5
    else:
        threshold = 5

    #capture the name of input data file and output data file
    inputFilename = sys.argv[1]
    outputFilename = sys.argv[2]

    #utilize functions to create sets, dictionaries and lists
    setMovie,setUser,lineCount = createset(inputFilename)
    dictMovie,dictUser,dictMovieRate,dictMovieTime = \
            createdictionaries(setMovie,setUser,inputFilename)
    list_movie,list_movie_currentMax,list_movie_currentMatchID, \
    list_movie_currentCommon = parallel_lists(setMovie)

    #initialize a global int variable to catch the value passed by
    #the function getcorrelation when the correlation is supposed
    #to be updated (when valid) and common count to be simultaneously updated
    global currentCommonCount
    currentCommonCount = 0

#start counting time
start = time.time()

#initialize correlation
currentCorrelation = 0
#iterate through movie list
for i in range(0,len(list_movie)-1):
    #compare movie with next movie til the end
    for j in range(i+1,len(list_movie)):
        #call the function getcorrelation by passing in two movies
        currentCorrelation = getcorrelation(list_movie[i],list_movie[j])
        #if the calculated correlation is bigger than what movie1
        #previously has, update every corresponding information
        if ( currentCorrelation > list_movie_currentMax[i] ):
            list_movie_currentMax[i] = currentCorrelation
            list_movie_currentCommon[i] = currentCommonCount
            list_movie_currentMatchID[i] = list_movie[j]
        #if the calculated correlation is bigger than what movie2
        #previously has, update every corresponding information
        if ( currentCorrelation > list_movie_currentMax[j] ):
            list_movie_currentMax[j] = currentCorrelation
            list_movie_currentCommon[j] = currentCommonCount
            list_movie_currentMatchID[j] = list_movie[i]

#lastly, write to output file in ascending order of movie-id's.
#It is possibly (if applicable) followed by a parentheses enclosing the
#data for the single most similar movie: the movie id of the similar movie,
#the similarity coefficient for the two movies, and the number of common
# users that rated both movies.
f_write = open(outputFilename, "w")
for i in range(len(list_movie)):
    f_write.write(list_movie[i])
    if (list_movie_currentMatchID[i] is not None):
        f_write.write(' '+'('+ str(list_movie_currentMatchID[i]) + ',' +
        str(list_movie_currentMax[i]) + ',' +
        str(list_movie_currentCommon[i]) + ')'+'\n')
    else:
        f_write.write("\n")
f_write.close()

#finish counting time
end = time.time()

#print information to command line
print("Input MovieLens file: {}".format(inputFilename))
print("Output file for similarity data: {}".format(outputFilename))
print("Minimum number of common users: {}".format(threshold))
print("Read {0} lines with total of {1} movies and {2} users".format(lineCount \
,len(setMovie),len(setUser)))
print("Computed similarities in {} seconds".format(str(end-start)))
