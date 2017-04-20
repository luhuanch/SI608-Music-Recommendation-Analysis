import csv
import math

def cosine_data(ratio):
    with open('artists_users_playcount_ratio.csv', encoding='utf-8') as inf:
        incsv = csv.reader(inf)
        next(incsv)

        user_dic = {}
        artist_dic = {}
        count = 1
        # Cosine similarity when vector is 0, 1
        # for line in incsv:
        #     try:
        #         if float(line[3]) < ratio:
        #             continue
        #     except:
        #         pass
        #     if line[0] in artist_dic:
        #         if line[1] in user_dic:
        #             artist_dic[line[0]].append(user_dic[line[1]])
        #         else:
        #             artist_dic[line[0]].append(count)
        #     else:
        #         if line[1] in user_dic:
        #             artist_dic[line[0]] = [user_dic[line[1]]]
        #         else:
        #             artist_dic[line[0]] = [count]
        #
        #     if line[1] not in user_dic:
        #         user_dic[line[1]] = count
        #         count += 1
        for line in incsv:
            try:
                if float(line[3]) < ratio:
                    continue
            except:
                pass
            if line[0] in artist_dic:
                if line[1] in user_dic:
                    artist_dic[line[0]][user_dic[line[1]]] = line[3]
                else:
                    artist_dic[line[0]][count] = line[3]
            else:
                artist_dic[line[0]] = {}
                if line[1] in user_dic:
                    artist_dic[line[0]][user_dic[line[1]]] = line[3]
                else:
                    artist_dic[line[0]][count] = line[3]

            if line[1] not in user_dic:
                user_dic[line[1]] = count
                count += 1

    return artist_dic
# user_dic= {user:{1:ratio}}
# artist_dic = {artist:{1:ratio}}
with open('artists_cosine_similarity_new.csv', 'w', newline='', encoding='utf-8') as outf:
    outcsv = csv.writer(outf)
    outcsv.writerow(['artist1', 'artist2', 'cosine similarity'])

    artist_dic = cosine_data(0.1)

    for art1 in artist_dic.keys():
        art1_dict = artist_dic[art1]
        denom_art1 = 0
        for user in art1_dict.keys():
            denom_art1 = denom_art1 + float(art1_dict[user])*float(art1_dict[user])

        for art2 in artist_dic.keys():
            numerator = 0
            denominator = 0
            art2_dict = artist_dic[art2]

            denom_art2 = 0
            for user in art2_dict.keys():
                denom_art2 = denom_art2 + float(art2_dict[user])*float(art2_dict[user])

                if user in art1_dict.keys():
                    numerator = numerator + float(art1_dict[user])*float(art2_dict[user])

            denominator = math.sqrt(denom_art1)*math.sqrt(denom_art2)
            cosine = numerator / denominator
            outcsv.writerow([art1] + [art2] + [cosine])


    # done = []
    # for art1 in artist_dic.keys():
    #     for art2 in artist_dic.keys():
    #         if art1 == art2 or (art1, art2) in done or (art2, art1) in done:
    #             continue
    #
    #         numerator = len(set(artist_dic[art1]).intersection(artist_dic[art2]))
    #
    #         denominator = math.sqrt(len(artist_dic[art1]))*math.sqrt(len(artist_dic[art2]))
    #         cosine = numerator/denominator
    #
    #         outcsv.writerow([art1] + [art2] + [cosine])
    #
    #         done.append((art1, art2))
