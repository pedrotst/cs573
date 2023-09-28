import csv
import pandas as pd

from globals import *


if __name__ == "__main__":
    data = pd.read_csv("dating-binned.csv")
    sample = data.sample(random_state=47, frac=1, replace=False)

    test_frac = .2
    total_len = len(sample)
    test_len = int(test_frac*total_len)
    train_len = total_len - test_len

    print(test_len+train_len, total_len)

    train_sample = sample.head(train_len)
    test_sample = sample.tail(test_len-1)

    test_sample.to_csv("testSet.csv", index=False)
    train_sample.to_csv("trainingSet.csv", index=False)

    


    # data = pd.concat([data, testSample]).drop_duplicates(keep=False)
    # data = data.reset_index(drop=True)
    # df_grpby = data.groupby(list(data.columns))
    # idx = [x[0] for x in df_grpby.groups.values() if len(x) == 1]
    # data.reindex(idx)
    
