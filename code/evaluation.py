# from __future__ import division
import random
import csv

def check(x, y):
    for item in y:
        if x in item:
            return True
    return False

with open('test_data.csv', encoding='utf-8') as inf:
    r = csv.reader(inf)
    next(r)

    test_data = {}
    for line in r:
        test_data[line[0]] = line[1]

hot_artist_lst = []
artist_similarity = {}
with open('train_cosine_similarity.csv', encoding='utf-8') as infile_cosine:
    r = csv.reader(infile_cosine)
    next(r, None)
    for row in r:
        if row[0] not in hot_artist_lst:
            hot_artist_lst.append(row[0])
            artist_similarity[row[0]] = {}
            if float(row[2]) > 0 and float(row[2]) < 1:
                artist_similarity[row[0]][row[1]] = float(row[2])
        else:
            if float(row[2]) > 0 and float(row[2]) < 1:
                artist_similarity[row[0]][row[1]] = float(row[2])

sorted_artist_similarity = {}
for key in artist_similarity.keys():
    sorted_item = sorted(artist_similarity[key].items(), key=lambda x:x[1], reverse=True)
    sorted_artist_similarity[key] = sorted_item[:10]

# print sorted_artist_similarity

with open('train_data.csv', encoding='utf-8') as f:
    incsv = csv.reader(f)
    next(incsv)

    done = []
    first_line = next(incsv)

    # Initialization
    user = first_line[1]
    target = [(first_line[0], first_line[3])]
    # print target
    accuracy = 0
    count = 0
    for line in incsv:
        if line[1] == user:
            target.append((line[0], line[3]))
        else:
            length = len(target)
            if length > 0:
                # train_size = int(0.8*length)
                # train_data = random.sample(target, train_size)
                # test_data = [i[0] for i in target if i not in train_data]

                prediction = {}

                for item in target:
                    try:
                        artists = sorted_artist_similarity[item[0]]
                    except:
                        continue
                    for art in artists:
                        if check(art[0], target):
                            continue
                        if art[0] not in prediction:
                            prediction[art[0]] = float(art[1]) * float(item[1])
                        else:
                            prediction[art[0]] += float(art[1]) * float(item[1])

                # test_size = length - train_size
                sorted_prediction = sorted(prediction, key=lambda key: prediction[key], reverse=True)
                # result = sorted_prediction[:test_size]
                # result = sorted_prediction[:10]
                result = sorted_prediction[:50]
                # print (result)
                # print (len(result))
                # print (result)

                if test_data[user] in result:
                    accuracy += 1
                # accuracy += len(set(result).intersection(test_data))/len(test_data)
                count += 1

            user = line[1]
            target = [(line[0], line[3])]

print (accuracy/count)
