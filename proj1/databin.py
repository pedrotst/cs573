import csv

from globals import *

def binerize(dic):
    enc = {}
    u = 0

    for attr in continuos_valued:
        vals = [float(x[attr]) for x in dic]
        maxval = max(vals)

        if(attr == "age" or attr == "age_o"):
            if maxval > 58:
                maxval = 58
        elif (attr in maxval_ten):
            if maxval > 10:
                maxval = 10
        elif (attr == "interests_correlate"):
            if maxval > 1:
                maxval = 1

        bin_size = float(maxval / 5)
        # bins = [[], [], [], [], []]
        bins = [0, 0, 0, 0, 0]

        for val in vals:
            if val <= bin_size :
                # bins[0].append(val)
                bins[0] += 1
            elif bin_size < val <= 2*bin_size:
                # bins[1].append(val)
                bins[1] += 1
            elif 2*bin_size < val <= 3*bin_size:
                # bins[2].append(val)
                bins[2] += 1
            elif 3*bin_size < val <= 4*bin_size:
                # bins[3].append(val)
                bins[3] += 1
            else:
                # bins[4].append(val)
                bins[4] += 1
        
        print("{}: {}".format(attr, bins))
        enc[attr] = bins
        
    return enc;


if __name__ == "__main__":

    with open('dating.csv', 'r') as csvfile:
        dicdata = csv.DictReader(csvfile, delimiter=',')
        # print('age' in list(dicdata)[0].keys())

        bins = binerize(list(dicdata))
        # bins["binId"] = [0, 1, 2, 3, 4]
        # print(bins.keys())
        with open('dating-binned.csv', 'w') as writefile:
            writer = csv.writer(writefile)
            keylist = list(bins.keys())
            writer.writerow(["binId"] + keylist)

            for i in range(5):
                writer.writerow([i] + [bins[x][i] for x in keylist])