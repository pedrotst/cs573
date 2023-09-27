import csv

from globals import *


if __name__ == "__main__":
    with open('dating.csv', 'r') as csvfile:
        dicdata = csv.DictReader(csvfile, delimiter=',')