unquote_col = ["race", "race_o", "field"]
encoding_cols = ["gender", "race", "race_o", "field"]
preferences = ["attractive_important", "sincere_important", "intelligence_important", 
            "funny_important", "ambition_important", "shared_interests_important"]

preferences_partner = ["pref_o_attractive", "pref_o_sincere", "pref_o_intelligence", "pref_o_funny", "pref_o_ambitious",
                    "pref_o_shared_interests"]

rating_of_partner = ["attractive_partner", "sincere_partner", "intelligence_partner", "funny_partner",
                    "ambition_partner", "shared_interests_partner"]

continuos_valued = ["age","age_o","importance_same_race","importance_same_religion","pref_o_attractive",
                    "pref_o_sincere","pref_o_intelligence","pref_o_funny","pref_o_ambitious","pref_o_shared_interests",
                    "attractive_important","sincere_important","intelligence_important","funny_important",
                    "ambition_important", "shared_interests_important","attractive","sincere","intelligence","funny",
                    "ambition","attractive_partner","sincere_partner","intelligence_partner","funny_partner",
                    "ambition_partner","shared_interests_partner","sports","tvsports","exercise","dining","museums",
                    "art","hiking","gaming","clubbing","reading","tv","theater","movies","concerts","music","shopping",
                    "yoga","interests_correlate","expected_happy_with_sd_people","like"]

maxval_ten = [ "importance_same_race","importance_same_religion", "attractive","sincere","intelligence","funny",
                    "ambition","attractive_partner","sincere_partner","intelligence_partner","funny_partner",
                    "ambition_partner","shared_interests_partner","sports","tvsports","exercise","dining","museums",
                    "art","hiking","gaming","clubbing","reading","tv","theater","movies","concerts","music","shopping",
                    "yoga", "like", "expected_happy_with_sd_people"]

# Performs label encoding in the database
# input:  the whole database already preprocessed
# output: a dictionary of encodings, indexed by each __encoding_cols__
# each index of the dictionary is lexicographically ordered, therefore the label the position of the value in this list
def label_encode(dic, enc_cols):
    # initialize the encoding dictionary
    enc = {}
    for enc_col in enc_cols:
        # we use sets for the label encoding, this way we always only add one element
        # each column in encoding_cols have a different set of label encodings
        enc[enc_col] = set()

    for row in dic:
        for enc_col in enc_cols:
            enc[enc_col].add(row[enc_col])
    
    for enc_col in enc_cols:
        enc[enc_col] = list(enc[enc_col])
        enc[enc_col].sort()
        # I'm not sure if it's necessary to do the enumeration of each encoding here
        enc[enc_col] = enc[enc_col]

    return enc


# def init():
#     global unquote_col, encoding_cols, preferences, preferences_partner, rating_of_partner, continuos_valued, maxval_ten
# 
#     unquote_col = ["race", "race_o", "field"]
#     encoding_cols = ["gender", "race", "race_o", "field"]
#     preferences = ["attractive_important", "sincere_important", "intelligence_important", 
#                 "funny_important", "ambition_important", "shared_interests_important"]
# 
#     preferences_partner = ["pref_o_attractive", "pref_o_sincere", "pref_o_intelligence", "pref_o_funny", "pref_o_ambitious",
#                         "pref_o_shared_interests"]
# 
#     rating_of_partner = ["attractive_partner", "sincere_partner", "intelligence_partner", "funny_partner",
#                         "ambition_partner", "shared_interests_partner"]
# 
#     continuos_valued = ["age","age_o","importance_same_race","importance_same_religion","pref_o_attractive",
#                         "pref_o_sincere","pref_o_intelligence","pref_o_funny","pref_o_ambitious","pref_o_shared_interests",
#                         "attractive_important","sincere_important","intelligence_important","funny_important",
#                         "ambition_important", "shared_interests_important","attractive","sincere","intelligence","funny",
#                         "ambition","attractive_partner","sincere_partner","intelligence_partner","funny_partner",
#                         "ambition_partner","shared_interests_partner","sports","tvsports","exercise","dining","museums",
#                         "art","hiking","gaming","clubbing","reading","tv","theater","movies","concerts","music","shopping",
#                         "yoga","interests_correlate","expected_happy_with_sd_people","like"]
# 
#     maxval_ten = [ "importance_same_race","importance_same_religion", "attractive","sincere","intelligence","funny",
#                         "ambition","attractive_partner","sincere_partner","intelligence_partner","funny_partner",
#                         "ambition_partner","shared_interests_partner","sports","tvsports","exercise","dining","museums",
#                         "art","hiking","gaming","clubbing","reading","tv","theater","movies","concerts","music","shopping",
#                         "yoga", "like", "expected_happy_with_sd_people"]
