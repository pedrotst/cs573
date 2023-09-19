import csv

with open('dating-full.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar="'")
    print(reader.__next__())