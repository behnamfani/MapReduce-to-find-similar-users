# MapReduce-to-similar-users
Find similar users w.r.t the given votes for movie genres using MapReduce

## Description
MapReduce is a programming model and framework designed for processing and generating large-scale data sets in a parallel and distributed manner. The input data is divided into smaller chunks, and the *mapper* is applied to each chunk independently to produce a set of key-value pairs as intermediate outputs. After this phase, the framework shuffles and sorts the intermediate key-value pairs based on their keys to ensure that all values for a particular key end up at the same reducer. Then the *reducer* is applied to each group of key-value pairs with the same key to generate the final output. 

In this program, [mrjob](https://mrjob.readthedocs.io/en/latest/) is used to create two pairs of mapper-reducers to find similar users w.r.t movie genres based on their votes given to various movies with different genres. 

![](mapreduce_work.jpg)
*https://www.tutorialspoint.com/map_reduce/map_reduce_introduction.htm*

## Dataset

The full u data set: 100000 ratings by 943 users on 1682 items. Each user has rated at least 20 movies. Users and items are numbered consecutively from 1.  The data is randomly ordered. This is a tab-separated list of user id | item id | rating | timestamp | Genres. The time stamps are unix seconds since 1/1/1970 UTC. Genres are unknown, Action, Adventure, Animation, Children's, Comedy, Crime, Documentary, Drama, Fantasy, Film-Noir, Horror, Musical, Mystery, Romance, Sci-Fi, Thriller, War, and Western 

https://grouplens.org/datasets/movielens/100k/

## First Mapper-Reducer
In the dataset, each user has voted on some movies. And each movie belongs to one or more than one genre's classes. Thus, it is possible to extract the users' votes for these genres. 
In the first MapReduce, I find if a user likes or dislikes a genre. These are some examples of the first MapReduce output: (we use the ids of the users.)

[”15”, ”Romance”] ”like”

[”15”, ”Sci-fi”] ”dislike”

[”15”, ”Thriller”] ”dislike”

[”15”, ”War”] ”like”

[”16”, ”Action”] ”like”

[”16”, ”Adventure”] ”like”

[”16”, ”Animation”] ”like”

[”16”, ”Children”] ”like”

## Second First Mapper-Reducer
In the second MapReduce, I compare user i with j (in this project we compare 50 different pairs of users, but you can change it to compare each user with all the other users)
using **Jaccard similarity**.  These are some examples of the final MapReduce output:

[”17”, ”56”] ”Similar”

[”18”, ”54”] ”Similar”

[”19”, ”70”] ”Similar”

[”2”, ”88”] ”Similar”

[”20”, ”53”] ”dissimilar”

[”21”, ”100”] ”dissimilar”

[”22”, ”55”] ”Similar”

[1]: mapreduce_work.jpg
