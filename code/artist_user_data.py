#! python3
# -*- coding: utf-8 -*-
from openpyxl import load_workbook
import csv
import sys
import json

# increase the field_size_limit
# and avoid OverflowError
maxInt = sys.maxsize
decrement = True

while decrement:
    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True

wb = load_workbook(filename = 'data/artists_listeners_playcount.xlsx')
sheet_ranges = wb['artists_listeners_playcount.txt']

top_artist = []
for row in range(2, 301):
    top_artist.append(sheet_ranges['A' + str(row)].value.lower())

with open('data/usersha1-artmbid-artname-plays.tsv', encoding='utf-8') as inf, \
        open('artists_users_playcount.txt', 'w', encoding='utf-8') as outf:
    intsv = csv.reader(inf, delimiter='\t')

    temp = next(intsv)[0]
    user = {}
    artist = {}
    for line in intsv:
        if int(line[3]) <= 10:
            continue

        if line[2] in top_artist:
            if line[0] in user:
                artist[line[2]] = line[3]
            else:
                if artist:
                    user[temp] = artist
                    js = json.dumps(user)
                    outf.write(js)
                    outf.write('\n')

                artist = {}
                user = {}
                user[line[0]] = {}
                artist[line[2]] = line[3]
                temp = line[0]

with open('artists_users_playcount.txt', encoding='utf-8') as inf, \
    open('artists_users_playcount_ratio.csv', 'w', newline='', encoding='utf-8') as outf:
    outcsv = csv.writer(outf)
    outcsv.writerow(['artists', 'users', 'playcount', 'ratio'])

    for line in inf:
        line = line.strip()
        js = json.loads(line)
        for user, artist in js.items():
            tot_playcount = sum({int(x) for x in artist.values()})
            for key, value in artist.items():
                ratio = int(value)/tot_playcount
                outcsv.writerow([key] + [user] + [value] + [ratio])
