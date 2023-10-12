import csv
import copy

from globals import *

def getminmax(dic):
    minmax_dic = {}

    for attr in continuos_valued:
        # vals = [float(x[attr]) for x in dic]
        # maxval = max(vals)
        minval = 0
        # make sure that the values discretized in previous step will fall in [0,1]
        if(attr == "age" or attr == "age_o"):
            minval = 18
            maxval = 58
        elif (attr in maxval_ten):
            maxval = 10
        elif (attr in preferences+preferences_partner):
            maxval = 1
        elif (attr == "interests_correlate"):
            minval = -1
            maxval = 1
        minmax_dic[attr] = (minval, maxval)
    
    return minmax_dic;

def binerize(dic, bin_num):
    binned_dic = []

    minmax_dic = getminmax(dic)
    p = 0
    p1 = 0
    not_continuous = [attr for attr in dic[0].keys() if not (attr in continuos_valued)]

    for row in dic:
        newrow = {}
        for col in continuos_valued:
            p = 0
            minval, maxval = minmax_dic[col]
            bin_size = float((maxval - minval) / bin_num)
            val = float(row[col])

            if val < minval + bin_size :
                newrow[col] = 0
                p += 1

            for i in range(1, bin_num):
                if minval + i*bin_size <= val < minval + (i+1)*bin_size:
                    newrow[col] = i
                    p += 1

            if val >= minval + bin_num*bin_size:
                newrow[col] = bin_num-1
                p += 1

            if (p != 1):
                print("p is {} for attr: {} val: {}".format(p, col, val))

        for attr in not_continuous:
            newrow[attr] = row[attr]


        binned_dic.append(copy.deepcopy(newrow))
        
    return binned_dic;

def printbinsizes(binned_dic):
    for attr in continuos_valued:
        binsizes = [0, 0, 0, 0, 0]
        for row in binned_dic:
            for i in range(5):
                if row[attr] == i:
                    binsizes[i] += 1
        print("{}: {}".format(attr, binsizes))

def bin(bin_num):
    with open('data/dating.csv', 'r') as csvfile:
        dicdata = csv.DictReader(csvfile, delimiter=',')
        binned = binerize(list(dicdata), bin_num)
        with open('data/dating-binned.csv', 'w') as writefile:
            writer = csv.DictWriter(writefile, binned[0].keys())
            writer.writeheader()
            writer.writerows(binned)
        return binned

if __name__ == "__main__":
    binned = bin(5)
    printbinsizes(binned)