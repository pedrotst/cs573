import csv
from globals import *
import databin as databin

from statistics import mean
import numpy as np
import matplotlib.pyplot as plt


# preference_scores_of_participants: [attractive_important, sincire_important, intellignce_important, funny_important,
#   ambition_important, shared_interests_important

# preference_scores_of_partner: pref_o_attractive, pref_o_sincere, pref_o_intelligence, pref_o_funny, pref_o_ambitious,
#   pref_o_shared_interests

# continuous_valued_columns: not [ gender, rance, race_o, samerace, field, decision ]

# rating_of_partner_from_participant: attractive_partner, sincere_partner, intelligence_partner, funny_partner,
#   ambition_partner, shared_interests_partner


def normalize(dic, prefs):
    total = 0

    # calculate total
    for row in dic:
        for preference in prefs:
            total += float(row[preference])

        # normalize
        for preference in prefs:
            row[preference] = float(row[preference]) / total
        total = 0
    

    return dic

# Unquotes the columns defined in __unquote_col__
# input: a row of dating-full in the form of dictionary
# output: (count, row)
#       count: number of unquoted cells
#       row: post processesd quote
def unquote(row):
    count = 0
    for col in unquote_col:
        cell = row[col]
        if cell.startswith("'") and cell.endswith("'") and len(cell) > 1:
            cell = cell.strip("'")
            count += 1
        if cell.startswith('"') and cell.endswith('"') and len(cell) > 1:
            cell = cell.strip('"')
            count += 1
        row[col] = cell
    return (count, row)

# Lowercases the __field__ column
# input: a row of dating-full in the form of a dictionary
# output: (count, row)
#       count: number of 
def tolower_field(row):
    count = 0
    if(not row["field"].islower()):
        count += 1
        row["field"] = row["field"].lower()
    return(count, row)

# Processes a dictionary by doing the following operations:
# 1 - unquote cells in unquote_col
# 2 - convert values in column field to lowercase
# input: csvDicReader
# output: (lower_count count, encodings, out_dic)
#       unq_count: number of unquoted cells
#       unq_count: number of lower cased field cells
#       label_encodings: encodings for the columns in encodings_val
#       outdic: preprocessed dictionary 
def preprocess(in_dic):
    unq_count = 0
    lower_count = 0
    out_dic = []
    for row in in_dic:
        c, row = unquote(row)
        c1, row = tolower_field(row)
        unq_count += c
        lower_count += c1
        out_dic.append(row)
    
    label_encodings = label_encode(out_dic, encoding_cols)
    out_dic = normalize(out_dic, preferences)
    out_dic = normalize(out_dic, preferences_partner)
    out_dic = encode_dic(out_dic, encoding_cols, label_encodings)
    return (unq_count, lower_count, label_encodings, out_dic)

def print_encodings(enc):
    for enc_col in encoding_cols:
        for id, val in enumerate(enc[enc_col]):
            if val == 'male' or (val == 'European/Caucasian-American' and enc_col == 'race') or (val == 'Latino/Hispanic American' and enc_col == 'race_o') or val == 'law':
                print("Value assigned for {} in column {}: {}".format(val, enc_col, id))
            

def print_means(dic):
    for pref in preferences + preferences_partner:
        col = [row[pref] for row in dic]
        print("Mean of {}: {}".format(pref, round(mean(col), 2)))


if __name__ == "__main__":
    with open('data/dating-full.csv', newline='') as csvfile:
        fulldata = csv.DictReader(csvfile, delimiter=',')
        unq_count, lower_count, label_encodings, dicdata = preprocess(fulldata)
        print("Quotes removed from", unq_count, "cells")
        print("Standardized", lower_count, "cells to lower case")
        print_encodings(label_encodings)
        print_means(dicdata)
        with open('data/dating.csv', 'w') as writefile:
            writer = csv.DictWriter(writefile, dicdata[0].keys())
            writer.writeheader()
            writer.writerows(dicdata)
        # plot_preferences_gender(dicdata)
        # second_date_by_rating(dicdata)
                            
