import re
from collections import OrderedDict
import numpy as np
from brain.tweet_analysis import tweet_analysis_function

def remove_hashtag(movie_name):
    for i in movie_name:
        if i=="#":
            movie_name=movie_name[1:len(movie_name)]
    return movie_name

def tweet_analysis_function(movie_name):
    return "Twitter Analysis Output for: "+movie_name

def levenshtein_ratio_and_distance(s, t, ratio_calc = True):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions    
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        # print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        return (distance[row][col])

def remove_repetitions(a):
    i=0
    while i<len(a)-1:
       if a[i]==a[i+1] or a[i]==" ":
           a=a[0:i]+a[i+1:len(a)]
           i-=1
       a=a[0:len(a)]
       i+=1
    return a

movies=["war","joker","rdxlove","geminiman","chanakya","gaddalakondaganesh",
        "theskyispink","vadaladu","evvarikeecheppoddu","rajugarigadhi","dreamgirl",
        "chhichhore","maleficent","diego","thelionking","abominable","angrybirds",
        "syeraa","weatheringwithyou","ratnakar","manoharam","avatar","titanic","missionmangal",
        "asuran","adhyaksha","ellidde","kiss","pailwaan","manoharam","nammaveetupillai",
        "kurukshetra","ratnakar","petromax","aruvam","gettha","gumnaami","lungi","vrithra",
        "loveactiondrama","porinjumariyam","bharaate","inject","devarubekagiddare","siddhiseere",
        "gnanam","kaappaan","chaati"]

freq_words=["in","at","the","and","if","of","then","that","review","movie","hit","superhit",
            "blockbuster","mania","boxoffice"]

def find_prefix(a):
    found_freq_words={}
    for i in freq_words:
        if a.find(i)>-1:
            found_freq_words[i]=a.find(i)
    return found_freq_words

def movies_lev_matched(ratios,match):
    movies_matched={}
    for key, value in ratios.items():
        if value>match:
            movies_matched[key]=value
    return movies_matched

def analyse_movie(movie_name):
    movie_name=remove_hashtag(movie_name)
    ratios={}
    for i in movies:
        ratios[i]=levenshtein_ratio_and_distance(i,movie_name)

    ratios=OrderedDict(sorted(ratios.items(), key=lambda kv:kv[1], reverse=True))

    movies_matched=movies_lev_matched(ratios,0.9)
    
    if len(movies_matched)==1:
        movie_matched=list(movies_matched.keys())[0]
        count_sentiment=tweet_analysis_function(movie_matched)
        return count_sentiment
    elif len(movies_matched)>1:
        return ("More than two movies matched.")
    elif len(movies_matched)<1:
        new_movie_name=remove_repetitions(movie_name)
        new_movies={}
        for i in movies:
            new_movies[remove_repetitions(i)]=i
        ratios={}
        for i in new_movies.keys():
            ratios[i]=levenshtein_ratio_and_distance(i,new_movie_name)

        ratios=OrderedDict(sorted(ratios.items(), key=lambda kv:kv[1], reverse=True))
        movies_matched=movies_lev_matched(ratios,0.9)
        
        if len(movies_matched)==1:
            movie_matched=list(movies_matched.keys())[0]
            count_sentiment=tweet_analysis_function(new_movies[movie_matched])
            return count_sentiment
        elif len(movies_matched)>1:
            return ("More than two movies matched.")
        elif len(movies_matched)<1:
            #return ratios #fails for pahelwan:0.8, sky is pink:0.85,
            for i in movies:
                pass

movie_name=input("Enter movie name: ")
review=analyse_movie(movie_name)
print(review)
