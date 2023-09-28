import csv
import pandas as pd

from globals import *

""" inputs
        t_frac : percentage of data used for testing
        data   : data as pandas Dataframe
    output (test_sample, train_sample) pandas dataframes split into test and training data
        
"""
def sample(t_frac, data):
    sample = data.sample(random_state=47, frac=1, replace=False)

    test_frac = t_frac
    total_len = len(sample)
    test_len = int(test_frac*total_len)
    train_len = total_len - test_len

    train_sample = sample.head(train_len)
    test_sample = sample.tail(test_len-1)
    return (test_sample, train_sample)


if __name__ == "__main__":
    data = pd.read_csv("dating-binned.csv")

    test_sample, train_sample = sample(.2, data)

    test_sample.to_csv("testSet.csv", index=False)
    train_sample.to_csv("trainingSet.csv", index=False)
