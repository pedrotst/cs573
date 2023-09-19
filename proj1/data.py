import csv

# preference_scores_of_participants: [attractive_important, sincire_important, intellignce_important, funny_important,
#   ambition_important, shared_interests_important

# preference_scores_of_partner: pref_o_attractive, pref_o_sincere, pref_o_intelligence, pref_o_funny, pref_o_ambitious,
#   pref_o_shared_interests

# continuous_valued_columns: not [ gender, rance, race_o, samerace, field, decision ]

# rating_of_partner_from_participant: attractive_partner, sincere_partner, intelligence_partner, funny_partner,
#   ambition_partner, shared_interests, partner

unquote_col = ["race", "race_o", "field"]
encoding_cols = ["gender", "race", "race_o", "field"]

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


# Performs label encoding in the database
# input:  the whole database already preprocessed
# output: a dictionary of encodings, indexed by each __encoding_cols__
# each index of the dictionary is lexicographically ordered, therefore the label the position of the value in this list

def label_encode(dic):
    # initialize the encoding dictionary
    enc = {}
    for enc_col in encoding_cols:
        # we use sets for the label encoding, this way we always only add one element
        # each column in encoding_cols have a different set of label encodings
        enc[enc_col] = set()

    for row in dic:
        for enc_col in encoding_cols:
            enc[enc_col].add(row[enc_col])
    
    for enc_col in encoding_cols:
        enc[enc_col] = list(enc[enc_col])
        enc[enc_col].sort()
        # I'm not sure if it's necessary to do the enumeration of each encoding here
        enc[enc_col] = enumerate(enc[enc_col])

    return enc

def print_encodings(enc):
    for enc_col in encoding_cols:
        for id, val in enc[enc_col]:
            print("Value assigned for {} in column {}: {}".format(val, enc_col, id))
            

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
    
    label_encodings = label_encode(out_dic)
    return (unq_count, lower_count, label_encodings, out_dic)



with open('dating-full.csv', newline='') as csvfile:
    fulldata = csv.DictReader(csvfile, delimiter=',')
    unq_count, lower_count, label_encodings, dicdata = preprocess(fulldata)
    # print(dicdata[48])
    print("Quotes removed from", unq_count, "cells")
    print("Standardized", lower_count, "cells to lower case")
    print_encodings(label_encodings)

