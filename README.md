# MapReduce-to-similar-users
A Mapreduce approach using mrjob library to find the users with the same taste of the genres of different movies.

In our dataset, each user has voted on some movies. And each movie belongs to one or more than one genres' classes. Thus, we can extract the users' votes to these genres. 
In the first Mapreduce, we find if a user likes or dislikes a genre. These are some examples of the first Mapreduce output: (we use the ids of the users.)

[”15”, ”Romance”] ”like”

[”15”, ”Sci-fi”] ”dislike”

[”15”, ”Thriller”] ”dislike”

[”15”, ”War”] ”like”

[”16”, ”Action”] ”like”

[”16”, ”Adventure”] ”like”

[”16”, ”Animation”] ”like”

[”16”, ”Children”] ”like”

In the second Mapreduce, we compare user i with j (in this project we compare 50 different pairs of users, but you can change it to compare each user with all the other users)
using Jaccard similarity.  These are some examples of the final Mapreduce output:

[”17”, ”56”] ”Similar”

[”18”, ”54”] ”Similar”

[”19”, ”70”] ”Similar”

[”2”, ”88”] ”Similar”

[”20”, ”53”] ”dissimilar”

[”21”, ”100”] ”dissimilar”

[”22”, ”55”] ”Similar”

You can find the description for the key and values of different mappers and reducers in the code's comment.
