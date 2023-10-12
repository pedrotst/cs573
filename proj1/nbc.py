from globals import *
import pandas as pd

import databin
import split
import plots

def nbc(t_frac, bin_num):
    fulldata = pd.read_csv("data/dating.csv").to_dict('records')
    # print(fulldata)
    label_encodings = label_encode(fulldata, encoding_cols)
    # print(label_encodings)

    train = pd.read_csv("data/trainingSet.csv")
    train = train.sample(random_state=47, frac=t_frac, replace=False)

    dec_true = train[train['decision'] == 1]
    dec_false = train[train['decision'] == 0]
    # +5 is for laplacian smoothing
    # i.e. we are adding one extra element in each bin
    dec_0 = len(dec_false) + bin_num
    dec_1 = len(dec_true) + bin_num

    total_size = dec_0 + dec_1

    P0 = dec_0 / total_size
    P1 = dec_1 / total_size

    # print("P0 ==", P0)
    # print("P1 ==", P1)
    # print("P0+P1 ==", P0+P1)
    # print(total_size)
    probs = {}

    for attr in continuos_valued:
        probs[attr] = []
        for i in range(bin_num):
            deci_true = dec_true[dec_true[attr] == i]
            deci_false = dec_false[dec_false[attr] == i]
            probs[attr].append(((len(deci_true)+1) / dec_1, (len(deci_false)+1) / dec_0))
    
    #print(train.columns)
    c = continuos_valued + ["Unnamed: 0", "decision"]
    not_continuous = [attr for attr in train.columns if not (attr in c)]

    # print(train.iterrows())
    for attr in not_continuous: 
        if attr in label_encodings.keys():
            maxlabel = max(label_encodings[attr])
        else:
            maxlabel = max([x[attr] for (i, x) in train.iterrows()])
        # print("attr: {}, maxlabel: {}".format(attr, maxlabel))
        probs[attr] = []
        for i in range(maxlabel+1):
            deci_true = dec_true[dec_true[attr] == i]
            deci_false = dec_false[dec_false[attr] == i]
            probs[attr].append(((len(deci_true)+1)/ (len(dec_true)+maxlabel), (len(deci_false)+1)/(len(dec_false)+maxlabel)))

    
    vals = []
    for attr in probs:
        s_1, s_0 = 0, 0
        for t,f in probs[attr]:
            s_1 += t
            s_0 += f
        vals.append((s_1, s_0))

    # print(set(vals))

    probs['decision'] = (dec_1/total_size, dec_0/total_size)

    
    #print(probs)
    return probs;

def accuracy(probs, data):
    total_data = len(data)
    total_correct = 0

    for i, row in data.iterrows():
        dec_1, dec_0 = probs['decision']
        for attr in data:
            if attr == 'decision': continue
            bin = row[attr]
            try: 
                bin_1, bin_0 = probs[attr][bin]
            except IndexError as e:
                print(f"{e}")
                print("attr: {} bin: {}, bin_size: {}".format(attr, bin, len(probs[attr])))
                print(probs[attr])
                exit()
            dec_1 *= bin_1
            dec_0 *= bin_0
        classification = 1 if dec_1 > dec_0 else 0
        if classification == row['decision']:
            total_correct += 1
    acc = total_correct / total_data

    return acc;

def many_bins():
    bin_nums = [2, 5, 10, 50, 100, 200]
    train_accs = []
    test_accs = []

    for i in bin_nums:
        databin.bin(i)
        split.do_sample()

        probs = nbc(1, i)
        train = pd.read_csv("data/trainingSet.csv")
        test = pd.read_csv("data/testSet.csv")
        train_acc = accuracy(probs, train)
        test_acc = accuracy(probs, test)

        print("Bin size: ", i)
        print("Training accuracy: {:.2f}".format(train_acc))
        print("Testing accuracy: {:.2f}".format(test_acc))
        train_accs.append(train_acc)
        test_accs.append(test_acc)

    plots.plot_nbc_bins(bin_nums, train_accs, test_accs)

def many_fracs():
    F = [0.01, 0.1, 0.2, 0.5, 0.6, 0.75, 0.9, 1]
    train_accs = []
    test_accs = []


    for i in F:
        databin.bin(5)
        split.do_sample()

        probs = nbc(i, 5)
        train = pd.read_csv("data/trainingSet.csv")
        test = pd.read_csv("data/testSet.csv")
        print("running many_fracs with i=", i)
        train_acc = accuracy(probs, train)
        print("test accuracy ran well")
        test_acc = accuracy(probs, test)

        print("Sample Size: ", i)
        print("Training accuracy: {:.2f}".format(train_acc))
        print("Testing accuracy: {:.2f}".format(test_acc))
        train_accs.append(train_acc)
        test_accs.append(test_acc)

    plots.plot_nbc_samples(F, train_accs, test_accs)

if __name__ == "__main__":
    many_fracs()
    # i = 5

    # databin.bin(i)
    # split.do_sample()

    # probs = nbc(1, i)
    # train = pd.read_csv("trainingSet.csv")
    # test = pd.read_csv("testSet.csv")
    # train_acc = accuracy(probs, train)
    # test_acc = accuracy(probs, test)

    # print("Bin size: ", i)
    # print("Training accuracy: {:.2f}".format(train_acc))
    # print("Testing accuracy: {:.2f}".format(test_acc))

