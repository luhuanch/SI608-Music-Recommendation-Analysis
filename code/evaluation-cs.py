import csv, operator, sys, json, getpass
import numpy as np
reload(sys)
sys.setdefaultencoding('utf-8')
csv.field_size_limit(sys.maxsize)

recommend_number = 5 # how many similar artists you recommend based on one artist
listen_count_threshold = 50 # how many times a qualified user listen to a hot artist
max_artists_num = 50 # how many hot artist a qualified user listened
min_artists_num = 10
ramdom_sample_size = 10 # how many artists to sample

hot_artist_lst = []
artist_similarity = {}

with open('artists_cosine_similarity.csv', 'rU') as infile_cosine:
    r = csv.reader(infile_cosine, delimiter = ',')
    next(r, None)
    for row in r:
        if row[0] not in hot_artist_lst:
            hot_artist_lst.append(row[0])
            artist_similarity[row[0]] = {}
            if float(row[2]) > 0:
                artist_similarity[row[0]][row[1]] = float(row[2])
        else:
            if float(row[2]) > 0:
                artist_similarity[row[0]][row[1]] = float(row[2])
        if row[1] not in hot_artist_lst:
            hot_artist_lst.append(row[1])
            artist_similarity[row[1]] = {}
            if float(row[2]) > 0:
                artist_similarity[row[1]][row[0]] = float(row[2])
        else:
            if float(row[2]) > 0:
                artist_similarity[row[1]][row[0]] = float(row[2])

infile_cosine.close()

for k in artist_similarity:
    if len(artist_similarity[k]) > recommend_number:
        sorted_tuple_lst = sorted(artist_similarity[k].items(), key = operator.itemgetter(1), reverse = True)
        artist_similarity[k] = {}
        for tup in sorted_tuple_lst[:recommend_number]:
            artist_similarity[k][tup[0]] = tup[1]

outfile = open('artist_similar.json','w')
outfile.write(json.dumps(artist_similarity))
outfile.close()

user_artist_playcount = {}
with open('usersha1-artmbid-artname-plays.tsv', 'rU') as infile_user:
    r = csv.reader(infile_user, delimiter = '\t')
    for row in r:
        if (row[2] in hot_artist_lst) and (int(row[3]) > listen_count_threshold):
            if row[0] not in user_artist_playcount:
                user_artist_playcount[row[0]] = {}
                user_artist_playcount[row[0]][row[2]] = int(row[3])
            else:
                user_artist_playcount[row[0]][row[2]] = int(row[3])
infile_user.close()

qualified_user = {}
for user in user_artist_playcount:
    if len(user_artist_playcount[user]) <= max_artists_num and len(user_artist_playcount[user]) >= min_artists_num:
        qualified_user[user] = user_artist_playcount[user]

outfile = open('qualified_user.json','w')
outfile.write(json.dumps(qualified_user))
outfile.close()

accuracy_lst = []
for user in qualified_user:
    real_artists = qualified_user[user].keys()
    random_artists = np.random.choice(real_artists, ramdom_sample_size, replace = False)
    rest_real_artists = real_artists
    for artist in random_artists:
        rest_real_artists.remove(artist)
    recommend_artists = []
    for artist in random_artists:
        recommend_artists += artist_similarity[artist].keys()
    score = 0
    for artist in rest_real_artists:
        if artist in recommend_artists:
            score += 1
    accuracy_lst.append(float(score)/len(rest_real_artists))

print "Recommend Number:",recommend_number
print "Listen Count Threshold:",listen_count_threshold
print "Max Artists Num:",max_artists_num
print "Min Artists Num:",min_artists_num
print "Ramdom Sample Size:",ramdom_sample_size
print "Testing Data Size (# Users):",len(qualified_user)
print "Accuracy:",reduce(lambda x, y: x + y, accuracy_lst) / len(accuracy_lst)
