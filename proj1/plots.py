import csv

from statistics import mean
from globals import *

import numpy as np
import matplotlib.pyplot as plt


def plot_preferences_gender(dic):
    males = [row for row in dic if row['gender'] == 'male']
    females = [row for row in dic if row['gender'] == 'female']

    males_preferences = {}
    females_preferences = {}
    plt.tight_layout()
    # fig = plt.figure(figsize=(5,5))
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    X = np.arange(len(preferences))
    r = 0
    barwidth = .9
    barlocs = [
        [1, 2], 
        [4, 5], 
        [7, 8], 
        [10, 11], 
        [13, 14], 
        [16, 17]]
    # colors = [(1,0,0,0), (0,1,0,0), (0,0,1,0), (1,0,0.8,0.2), (0.75,1,0,0.1), (0,0.5,1,0.1)]
    colors = [
        (0.9, 0.1, 0, 0.1),      # Soft Blue
        (0.1, 0.9, 0.1, 0.1),    # Rosy Pink
        (0, 0.1, 0.9, 0.1),      # Bright Yellow-Green
        (0.6, 0, 0.5, 0.1),      # Turquoise
        (0.1, 0.6, 0, 0.1),      # Mauve
        (0.9, 0.3, 0.1, 0.2)     # Coral Red
    ]

    for (pref, c, barloc) in zip(preferences, colors, barlocs):
        male_pref = [float(row[pref]) for row in males]
        female_pref = [float(row[pref]) for row in females]

        males_preferences[pref] = mean(male_pref)
        females_preferences[pref] = mean(female_pref)
        print("\nPreference: ", pref)
        print("\rMale: ", males_preferences[pref])
        print("\rFemale: ", females_preferences[pref])

        ax.bar(barloc[0], males_preferences[pref], 
               width=barwidth, color='b', label=pref)

        ax.bar(barloc[1], females_preferences[pref], 
               width=barwidth, color='r', label=pref)

    # plt.legend()
    # ax.set_aspect('equal')

    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')

    plt.xticks([mean(barloc) for barloc in barlocs], preferences, rotation=90)
    # plt.xticks([r + barwidth for r in range(len(preferences))], preferences, rotation=90)

    # Adjust the margins
    # plt.subplots_adjust(bottom= 0.2, top = 0.8)

    plt.legend(["Male", "Female"])

    plt.savefig('graphs/importance.png', bbox_inches = 'tight')
    #plt.show()

    return;


def second_date_by_rating(dic):
    # label_encodings = label_encode(dic, rating_of_partner)
    # print(label_encodings)


    for rating in rating_of_partner:
        # print()
        plt.tight_layout()
        fig = plt.figure()
        successes = []
        labels = [float(x) for x in label_encodings[rating]]
        labels.sort()
        print(rating, labels)

        for label in labels:
            all_labels = [(float(x[rating]), x["decision"]) for x in dic if float(x[rating]) == label]
            positive_labels = [val for (val, dec) in all_labels if int(dec) == 1]

            success_rate = 0 if len(all_labels) == 0 else len(positive_labels) / len(all_labels)
            successes.append(success_rate)

            # print("Rating: {}, label: {}, success_rate: {}".format(rating, label, success_rate))

        plt.scatter(labels, successes)
        plt.title(rating)
        plt.xlabel("Value")
        plt.ylabel("Success Rate")
        plt.savefig("graphs/"+rating+".png", bbox_inches = 'tight')


    return;

def plot_nbc_bins(bin_nums, train_accs, test_accs):
    plt.tight_layout()
    fig = plt.figure()


    barlocs = [
        [1, 2], 
        [4, 5], 
        [7, 8], 
        [10, 11], 
        [13, 14], 
        [16, 17]]

    barwidth = .9

    for barloc, train, test in zip(barlocs, train_accs, test_accs):
        plt.bar(barloc[0], train, width=barwidth, color='b', label="Training Accuracy")
        plt.bar(barloc[1], test, width=barwidth, color='r', label="Testing Accuracy")

    plt.xticks([mean(barloc) for barloc in barlocs], bin_nums)
    # plt.xticks(y_pos, bin_nums)

    plt.xlabel("Bin Size")
    plt.ylabel("Model Accuracy")
    plt.legend(["Training Accuracy", "Testing Accuracy"])
    ax = plt.gca()
    ax.set_ylim([.5, 1])

    plt.savefig('graphs/bin_accuracies.png')


    return;

def plot_nbc_samples(bin_nums, train_accs, test_accs):
    plt.tight_layout()
    fig = plt.figure()


    barlocs = [
        [1, 2], 
        [4, 5], 
        [7, 8], 
        [10, 11], 
        [13, 14], 
        [16, 17],
        [19, 20],
        [22, 23]
        ]

    barwidth = .9

    for barloc, train, test in zip(barlocs, train_accs, test_accs):
        plt.bar(barloc[0], train, width=barwidth, color='b', label="Training Accuracy")
        plt.bar(barloc[1], test, width=barwidth, color='r', label="Testing Accuracy")

    plt.xticks([mean(barloc) for barloc in barlocs], bin_nums)
    # plt.xticks(y_pos, bin_nums)

    plt.xlabel("Sample Size")
    plt.ylabel("Model Accuracy")
    plt.legend(["Training Accuracy", "Testing Accuracy"])
    ax = plt.gca()
    ax.set_ylim([.5, 1])
    plt.savefig('graphs/sample_accuracies.png')


    return;

if __name__ == "__main__":
    with open('data/dating.csv', 'r') as csvfile:
        dicdata = csv.DictReader(csvfile, delimiter=',')
        dicdata = list(dicdata)

        plot_preferences_gender(dicdata)
        second_date_by_rating(dicdata)