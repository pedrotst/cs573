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

def binerize(dic):
    binned_dic = []

    minmax_dic = getminmax(dic)
    p = 0
    p1 = 0

    for row in dic:
        newrow = {}
        for col in continuos_valued:
            minval, maxval = minmax_dic[col]
            bin_size = float((maxval - minval) / 5)
            # print("{}: minval = {}, maxval = {}".format(col, minval, maxval))
            val = float(row[col])
            if(col=="reading" and p == 0):
                print("{}: minval = {}, maxval = {}".format(col, minval, maxval))
                p = 1
            if(col=="gaming" and p1 == 0):
                print("{}: minval = {}, maxval = {}".format(col, minval, maxval))
                p1 = 1

            
            if val < minval + bin_size :
                newrow[col] = 0
            elif bin_size + minval <= val < minval + 2*bin_size:
                newrow[col] = 1
            elif 2*bin_size + minval <= val < minval + 3*bin_size:
                newrow[col] = 2
            elif 3*bin_size + minval <= val < minval + 4*bin_size:
                newrow[col] = 3
            else:
                newrow[col] = 4
        newrow["decision"] = row["decision"]
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


if __name__ == "__main__":
    with open('dating.csv', 'r') as csvfile:
        dicdata = csv.DictReader(csvfile, delimiter=',')
        # print('age' in list(dicdata)[0].keys())

        binned = binerize(list(dicdata))
        # bins["binId"] = [0, 1, 2, 3, 4]
        # print(bins.keys())
        # print(binned)
        printbinsizes(binned)
        # print(binned)
        with open('dating-binned.csv', 'w') as writefile:
            writer = csv.DictWriter(writefile, binned[0].keys())
            writer.writeheader()
            writer.writerows(binned)


            # keylist = list(bins.keys())
            # writer.writerow(["binId"] + keylist)

            # for key in bins.keys():
            #     for i in range(5):
            #         writer.writerow([str(key) + str(i)] + bins[key][i])