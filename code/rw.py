

datafile = open("artists_users_ratio.csv","r")
datafile.readline()
f = datafile.readlines()

def random_walk(data,user,step = 1):
    art_dic = {}
    for line in data:
        if line.split(",")[1] == user:
            art_dic[line.split(",")[0]] = float(line.split(",")[2])
    for i in range(step):
        user_dic = {}
        for art in art_dic:
            for line in data:
                if line.split(",")[0] == art:
                    if line.split(",")[1] not in user_dic:
                        user_dic[line.split(",")[1]] = art_dic[art]*float(line.split(",")[3])
                    else:
                        user_dic[line.split(",")[1]] += art_dic[art]*float(line.split(",")[3])
        art_dic={}
        for user in user_dic:
            for line in data:
                if line.split(",")[1] == user:
                    if line.split(",")[0] not in art_dic:
                        art_dic[line.split(",")[0]] = user_dic[user]*float(line.split(",")[2])
                    else:
                        art_dic[line.split(",")[0]] += user_dic[user]*float(line.split(",")[2])

    return art_dic

print random_walk(f,"0e9512560d29e11fdc54982960a4ba3afb168844")
