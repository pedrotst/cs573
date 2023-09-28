from globals import *
import pandas as pd

import split

def nbc(t_frac):
    train = pd.read_csv("trainingSet.csv")
    train = train.sample(random_state=47, frac=t_frac, replace=False)

    dec_true = train[train['decision'] == 1]
    dec_false = train[train['decision'] == 0]
    # +5 is for laplacian smoothing
    # i.e. we are adding one extra element in each bin
    dec_0 = len(dec_false) + 5
    dec_1 = len(dec_true) + 5

    total_size = dec_0 + dec_1

    P0 = dec_0 / total_size
    P1 = dec_1 / total_size

    # print("P0 ==", P0)
    # print("P1 ==", P1)
    # print("P0+P1 ==", P0+P1)
    # print(total_size)
    probs = {}

    for attr in train.columns:
        if attr == 'decision': continue
        probs[attr] = []
        for i in range(5):
            deci_true = dec_true[dec_true[attr] == i]
            deci_false = dec_false[dec_false[attr] == i]
            probs[attr].append(((len(deci_true)+1) / dec_1, (len(deci_false)+1) / dec_0))
    
    # vals = []
    # for attr in probs:
    #     s_1, s_0 = 0, 0
    #     for t,f in probs[attr]:
    #         s_1 += t
    #         s_0 += f
    #     vals.append((s_1, s_0))

    # print(set(vals))

    probs['decision'] = (dec_1, dec_0)

    
    # print(probs)
    return probs;

def accuracy(probs, data):
    total_data = len(data)
    total_correct = 0

    for i, row in data.iterrows():
        dec_1, dec_0 = probs['decision']
        for attr in data:
            if attr == 'decision': continue
            bin = row[attr]
            bin_1, bin_0 = probs[attr][bin]
            dec_1 *= bin_1
            dec_0 *= bin_0
        classification = 1 if dec_1 > dec_0 else 0
        if classification == row['decision']:
            total_correct += 1
    acc = total_correct / total_data

    return acc;

if __name__ == "__main__":

    train = pd.read_csv("trainingSet.csv")
    test = pd.read_csv("testSet.csv")

    probs = nbc(1)
    train_acc = accuracy(probs, train)
    test_acc = accuracy(probs, test)

    # Don't forget to put this on percentages
    print("Training accuracy: {:.2f}".format(train_acc))
    print("Testing accuracy: {:.2f}".format(test_acc))
