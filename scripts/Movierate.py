
import statistics as st
from mrjob.job import MRJob
from mrjob.step import MRStep
import random

'''
# Preprocessing on the data
# First we add the genre of each movie to our u_data file
genre = ['unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy'
    , 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-fi', 'Thriller', 'War', 'Western']

# Find the genre of the movies from u_item file and save it in movie_dict
movie_dic = {}
file1 = open('u_item.txt', 'r')
Lines = file1.readlines()

for i in Lines:
    line = i.rstrip('\n').split('|')
    genre_of_movie = line[-19:].copy()
    which_genre = []
    for j in range(len(genre_of_movie)):
        if genre_of_movie[j] == '1':
            which_genre.append(genre[j])
    movie_dic[line[0]] = which_genre

# Add genres of the movies to u_data file
file2_read = open('u_data.txt', 'r')
Lines = file2_read.readlines()
for i in range(len(Lines)):
    line = Lines[i].rstrip('\n').split('\t')
    string = " ".join(str(x) for x in line)
    this_genre = " ".join(str(x) for x in movie_dic[line[1]])
    string += ' ' + this_genre
    Lines[i] = string + '\n'

file2_write = open("u_data.txt", "w")
file2_write.writelines(Lines)
file2_write.close()
'''

# Building a dictionary to pair users for comparison. To speed up th comparison, we only compare a user with
# another random user. But it is obvious we can map a list of users to a user for the comparison in this dictionary.
user_comparison = {}
for i in range(50):
    a = random.randint(51, 100)
    while a in user_comparison.values():
        a = random.randint(51, 100)
    user_comparison[i+1] = a
    user_comparison[a] = i+1


class Similar_User(MRJob):

    def first_mapper(self, _, line):
        # We read and convert each line of the u_data file to a list with the name a
        # a[0] is the id of user, a[1] is the id of movie, a[2] is the rating for that movie, a[3] is the timestamp
        # From a[4] to the end of the array is the genres of this movie
        # In The mapper we combine the id of the user with each genre of that specific movie as the key, and the value
        # of the key is the rating for the movie
        a = line.split(' ')
        if int(a[0]) <= 100:
            id = a[0]
            rate = a[2]
            movie_genre = a[4:]
            for i in movie_genre:
                yield (id, i), int(rate)

    def first_reducer(self, key, values):
        # If the mean of the votes from user i to genre j is >= 3, it means this user likes the genre. o.w the user does
        # not like this genre. So the keys are the pairs of user-genre and the values are like or dislike.
        keys = [x for x in key]
        if st.mean(values) >= 3:
            yield (keys[0], keys[1]), "like"
        else:
            yield (keys[0], keys[1]), "dislike"

    def second_mapper(self, key, values):
        # Now we want to compare 50 pairs of user i-user j base on the genres. Thus, we produce the keys equal to
        # (user i, user j) with (id) user i < user j to have the same keys for these users in different mappers.
        # The value of the keys are the user, genre, and "like" or "dislike" base on the input of the mapper.
        global user_comparison
        keys = [x for x in key]
        a = user_comparison[int(keys[0])]
        if int(keys[0]) < 50:
            yield (keys[0], str(a)), (keys[0], keys[1], values)
        else:
            yield (str(a), keys[0]), (keys[0], keys[1], values)

    def second_reducer(self, key, values):
        # In this function we search and find the common genres that both users i and j from the input have voted to it.
        # If both users have the same taste of this genre, similar_vote is added by one.
        # Jaccard similarity is qual to similar_vote / all the common genre with same or different feelings from the
        # users (vote). So the output of every reducer is consist of a key = (user i, user j) and values = "Similar" or
        # "dissimilar" base on the result of the Jaccard similarity.
        values = [x for x in values]
        similar_voted, voted, result = 0, 0, 'dissimilar'
        for i in range(len(values)):
            x = values[i]
            for j in range(i+1, len(values)):
                y = values[j]
                if x[0] != y[0] and x[1] == x[1]:
                    if x[2] == y[2]:
                        similar_voted += 1
                    voted += 1
        if voted != 0:
            if similar_voted/voted >= 0.5:
                result = 'Similar'
        yield key, result

    def steps(self):
        return [
            MRStep(mapper=self.first_mapper,
                   reducer=self.first_reducer),
            MRStep(mapper= self.second_mapper,
                   reducer=self.second_reducer)
        ]


if __name__ == '__main__':
   Similar_User.run()

